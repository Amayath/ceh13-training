#!/usr/bin/env python3
"""Merge a module's notes+flashcards fragment into data/notes.json and data/flashcards.json.
Usage: python3 merge_content.py fragment.json
fragment.json shape: {"slug": "mod02", "sections": [...], "flashcards": [...]}
"""
import json
import sys
from pathlib import Path

DATA = Path("/Users/amayafontagne/ceh13-training/data")

def main():
    fragment = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    slug = fragment["slug"]

    notes = json.loads((DATA / "notes.json").read_text(encoding="utf-8"))
    notes[slug] = {"sections": fragment["sections"]}
    (DATA / "notes.json").write_text(json.dumps(notes, indent=2, ensure_ascii=False), encoding="utf-8")

    cards = json.loads((DATA / "flashcards.json").read_text(encoding="utf-8"))
    cards = [c for c in cards if c["module"] != slug]
    cards.extend(fragment["flashcards"])
    (DATA / "flashcards.json").write_text(json.dumps(cards, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Merged {slug}: {len(fragment['sections'])} sections, {len(fragment['flashcards'])} flashcards")

if __name__ == "__main__":
    main()
