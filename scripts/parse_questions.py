#!/usr/bin/env python3
"""Parse extracted CEHv13 exam text files into a unified questions.json bank."""
import json
import re
from pathlib import Path

TEXT_DIR = Path("/private/tmp/claude-501/-Users-amayafontagne/77817b04-5a18-4791-ae2d-880673b2d62e/scratchpad/ceh_text")
OUT_PATH = Path("/Users/amayafontagne/ceh13-training/data/questions.json")

BULLET = ""


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def parse_format_a(text: str, source: str):
    """'Question N:' / bullet options with '(Correct)' / 'Explanation' format."""
    blocks = re.split(r"\n(?=Question \d+:\n)", text)
    questions = []
    for block in blocks:
        m = re.match(r"Question (\d+):\n", block)
        if not m:
            continue
        qnum = m.group(1)
        body = block[m.end():]
        lines = body.split("\n")

        stem_lines, options, explanation_lines = [], [], []
        mode = "stem"
        current_option = None
        for line in lines:
            stripped = line.strip()
            if mode in ("stem", "options") and stripped == "Explanation":
                mode = "explanation"
                continue
            if mode == "stem":
                if stripped.startswith(BULLET):
                    mode = "options"
                    current_option = stripped[len(BULLET):].strip()
                    options.append(current_option)
                else:
                    stem_lines.append(line)
            elif mode == "options":
                if stripped.startswith(BULLET):
                    current_option = stripped[len(BULLET):].strip()
                    options.append(current_option)
                elif stripped == "":
                    continue
                else:
                    if options:
                        options[-1] = options[-1] + " " + stripped
            elif mode == "explanation":
                explanation_lines.append(line)

        stem = clean(" ".join(stem_lines))
        correct_index = None
        clean_options = []
        for i, opt in enumerate(options):
            is_correct = "(Correct)" in opt
            opt_clean = clean(opt.replace("(Correct)", ""))
            if is_correct:
                correct_index = i
            clean_options.append(opt_clean)

        explanation = clean(" ".join(explanation_lines))
        if stem and clean_options and correct_index is not None:
            questions.append({
                "id": f"{source}-{qnum}",
                "question": stem,
                "options": clean_options,
                "correctIndex": correct_index,
                "explanation": explanation,
                "source": source,
            })
    return questions


def parse_format_b(text: str, source: str):
    """Numbered '1. ... A. B. C. D. ... Ans:X' format (no explanation)."""
    blocks = re.split(r"\n(?=\d+\.\s)", text)
    questions = []
    letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
    for block in blocks:
        m = re.match(r"(\d+)\.\s", block)
        if not m:
            continue
        qnum = m.group(1)
        body = block[m.end():]

        ans_match = re.search(r"Ans[:;]?\s*([A-E])", body)
        if not ans_match:
            continue
        correct_letter = ans_match.group(1)
        body_before_ans = body[:ans_match.start()]

        opt_match = re.search(r"\n\s*A\.\s", body_before_ans)
        if not opt_match:
            continue
        stem = clean(body_before_ans[:opt_match.start()])
        opts_text = body_before_ans[opt_match.start():]

        raw_opts = re.split(r"\n\s*([A-E])\.\s", "\n" + opts_text)
        opts = {}
        for i in range(1, len(raw_opts), 2):
            letter = raw_opts[i]
            opt_text = raw_opts[i + 1] if i + 1 < len(raw_opts) else ""
            opts[letter] = clean(opt_text)

        if not stem or not opts or correct_letter not in opts:
            continue
        ordered_letters = sorted(opts.keys())
        options = [opts[l] for l in ordered_letters]
        correct_index = ordered_letters.index(correct_letter)

        questions.append({
            "id": f"{source}-{qnum}",
            "question": stem,
            "options": options,
            "correctIndex": correct_index,
            "explanation": "",
            "source": source,
        })
    return questions


def main():
    all_questions = []
    format_a_files = {
        "exam_set_2": "Exam Set 2",
        "exam_set_3": "Exam Set 3",
        "exam_set_4": "Exam Set 4",
        "practice_questions": "Practice Questions",
    }
    for fname, label in format_a_files.items():
        path = TEXT_DIR / f"{fname}.txt"
        if path.exists():
            text = path.read_text(encoding="utf-8")
            qs = parse_format_a(text, label)
            print(f"{label}: {len(qs)} questions")
            all_questions.extend(qs)

    dump_path = TEXT_DIR / "dump.txt"
    if dump_path.exists():
        text = dump_path.read_text(encoding="utf-8")
        qs = parse_format_b(text, "CEH v13 Dump")
        print(f"CEH v13 Dump: {len(qs)} questions")
        all_questions.extend(qs)

    # dedupe by normalized question text
    seen = set()
    deduped = []
    for q in all_questions:
        key = q["question"].lower()[:200]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(q)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(deduped, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Total unique questions: {len(deduped)} -> {OUT_PATH}")


if __name__ == "__main__":
    main()
