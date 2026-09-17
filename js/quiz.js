let ALL_QUESTIONS = [];
let MODULES = [];
let quizQueue = [];
let quizIndex = 0;
let quizScore = 0;
let quizAnswered = false;
let quizMode = "practice"; // "practice" | "exam" | "exam-short"
let userAnswers = [];      // exam modes: index per question, or null if unanswered
let examTimerInterval = null;
let examEndTime = null;

const EXAM_CONFIGS = {
  exam: { count: 125, seconds: 4 * 60 * 60, label: "Examen blanc" },
  "exam-short": { count: 50, seconds: 60 * 60, label: "Examen court" },
};

function getParam(name) {
  return new URLSearchParams(location.search).get(name);
}

async function initQuiz() {
  const session = await requireSession();
  if (!session) return;
  await Storage.init();

  const [questions, modules] = await Promise.all([
    fetch("data/questions.json").then(r => r.json()),
    fetch("data/modules.json").then(r => r.json()),
  ]);
  ALL_QUESTIONS = questions;
  MODULES = modules;

  const sources = [...new Set(ALL_QUESTIONS.map(q => q.source))].sort();
  const sourceSelect = document.getElementById("source-select");
  sources.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s;
    const count = ALL_QUESTIONS.filter(q => q.source === s).length;
    opt.textContent = s === "CEH v13 Dump" ? `${s} ⚠️ non vérifié (${count})` : `${s} (${count})`;
    sourceSelect.appendChild(opt);
  });
  sourceSelect.addEventListener("change", () => {
    document.getElementById("dump-hint").style.display = sourceSelect.value === "CEH v13 Dump" ? "block" : "none";
  });

  const moduleSelect = document.getElementById("module-select");
  const modulesWithQuestions = modules.filter(m => ALL_QUESTIONS.some(q => q.module === m.slug));
  modulesWithQuestions.forEach(m => {
    const opt = document.createElement("option");
    opt.value = m.slug;
    const count = ALL_QUESTIONS.filter(q => q.module === m.slug).length;
    opt.textContent = `${String(m.id).padStart(2, "0")} — ${m.title} (${count})`;
    moduleSelect.appendChild(opt);
  });

  const preselectModule = getParam("module");
  if (preselectModule && modulesWithQuestions.some(m => m.slug === preselectModule)) {
    moduleSelect.value = preselectModule;
  }

  const mistakeIds = getMistakeIds();
  const mistakesCheck = document.getElementById("mistakes-check");
  document.getElementById("mistakes-count").textContent = mistakeIds.size;
  if (mistakeIds.size === 0) mistakesCheck.disabled = true;

  document.getElementById("start-btn").addEventListener("click", () => startQuiz("practice"));
  document.getElementById("start-exam-btn").addEventListener("click", () => startQuiz("exam"));
  document.getElementById("start-short-exam-btn").addEventListener("click", () => startQuiz("exam-short"));
  document.getElementById("next-btn").addEventListener("click", nextQuestion);
  document.getElementById("quit-btn").addEventListener("click", () => {
    stopExamTimer();
    location.reload();
  });
  document.getElementById("restart-btn").addEventListener("click", () => location.reload());
}

function getMistakeIds() {
  const stats = Storage.getState().questionStats;
  return new Set(Object.keys(stats).filter(id => stats[id].lastCorrect === false));
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function startQuiz(mode) {
  quizMode = mode;

  if (mode === "exam" || mode === "exam-short") {
    const cfg = EXAM_CONFIGS[mode];
    quizQueue = shuffle(ALL_QUESTIONS).slice(0, Math.min(cfg.count, ALL_QUESTIONS.length));
  } else {
    const module = document.getElementById("module-select").value;
    const source = document.getElementById("source-select").value;
    const count = parseInt(document.getElementById("count-input").value, 10) || 20;
    const doShuffle = document.getElementById("shuffle-check").checked;
    const mistakesOnly = document.getElementById("mistakes-check").checked;

    let pool = ALL_QUESTIONS;
    if (module !== "all") pool = pool.filter(q => q.module === module);
    if (source !== "all") pool = pool.filter(q => q.source === source);
    if (mistakesOnly) {
      const ids = getMistakeIds();
      pool = pool.filter(q => ids.has(q.id));
    }
    pool = doShuffle ? shuffle(pool) : pool;
    quizQueue = pool.slice(0, Math.min(count, pool.length));
  }

  quizIndex = 0;
  quizScore = 0;
  userAnswers = new Array(quizQueue.length).fill(null);

  document.getElementById("setup-panel").style.display = "none";
  document.getElementById("result-panel").style.display = "none";
  document.getElementById("result-review").innerHTML = "";
  document.getElementById("quiz-panel").style.display = "block";

  const timerEl = document.getElementById("exam-timer");
  if (mode === "exam" || mode === "exam-short") {
    timerEl.style.display = "block";
    startExamTimer(EXAM_CONFIGS[mode].seconds);
  } else {
    timerEl.style.display = "none";
  }

  if (quizQueue.length === 0) {
    document.getElementById("q-text").textContent = "Aucune question ne correspond à cette sélection.";
    document.getElementById("q-options").innerHTML = "";
    document.getElementById("next-btn").disabled = true;
    return;
  }

  renderQuestion();
}

function startExamTimer(seconds) {
  examEndTime = Date.now() + seconds * 1000;
  updateExamTimer();
  examTimerInterval = setInterval(updateExamTimer, 1000);
}

function stopExamTimer() {
  if (examTimerInterval) clearInterval(examTimerInterval);
  examTimerInterval = null;
}

function updateExamTimer() {
  const remaining = Math.max(0, Math.round((examEndTime - Date.now()) / 1000));
  const h = String(Math.floor(remaining / 3600)).padStart(2, "0");
  const m = String(Math.floor((remaining % 3600) / 60)).padStart(2, "0");
  const s = String(remaining % 60).padStart(2, "0");
  const el = document.getElementById("exam-timer");
  el.textContent = `⏱ ${h}:${m}:${s}`;
  el.classList.toggle("warning", remaining <= 600 && remaining > 120);
  el.classList.toggle("danger", remaining <= 120);

  if (remaining <= 0) {
    stopExamTimer();
    finishQuiz();
  }
}

function renderQuestion() {
  quizAnswered = false;
  const q = quizQueue[quizIndex];
  const isExam = quizMode === "exam" || quizMode === "exam-short";
  const progressLabel = isExam ? EXAM_CONFIGS[quizMode].label : "Question";
  document.getElementById("quiz-progress").textContent =
    `${progressLabel} ${quizIndex + 1} / ${quizQueue.length}${!isExam ? " — Score: " + quizScore : ""}`;
  document.getElementById("q-source").textContent = q.source + (q.source === "CEH v13 Dump" ? " ⚠️" : "");
  document.getElementById("q-text").textContent = q.question;
  document.getElementById("q-explanation").style.display = "none";
  document.getElementById("q-explanation").textContent = "";
  document.getElementById("next-btn").disabled = isExam ? userAnswers[quizIndex] === null : true;

  const optsWrap = document.getElementById("q-options");
  optsWrap.innerHTML = "";
  q.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "option";
    btn.textContent = opt;
    if (isExam && userAnswers[quizIndex] === i) {
      btn.classList.add("selected");
    }
    btn.addEventListener("click", () => selectAnswer(i));
    optsWrap.appendChild(btn);
  });
}

function selectAnswer(i) {
  const q = quizQueue[quizIndex];
  const isExam = quizMode === "exam" || quizMode === "exam-short";

  if (isExam) {
    userAnswers[quizIndex] = i;
    if (!quizAnswered) {
      quizAnswered = true;
      Storage.recordQuestionResult(q.id, i === q.correctIndex);
    }
    document.querySelectorAll("#q-options .option").forEach((btn, idx) => {
      btn.classList.toggle("selected", idx === i);
    });
    document.getElementById("next-btn").disabled = false;
    return;
  }

  if (quizAnswered) return;
  quizAnswered = true;
  const correct = i === q.correctIndex;
  if (correct) quizScore += 1;
  Storage.recordQuestionResult(q.id, correct);

  const buttons = document.querySelectorAll("#q-options .option");
  buttons.forEach((btn, idx) => {
    btn.disabled = true;
    if (idx === q.correctIndex) btn.classList.add("correct");
    else if (idx === i) btn.classList.add("incorrect");
  });

  if (q.explanation) {
    const expl = document.getElementById("q-explanation");
    expl.style.display = "block";
    expl.textContent = q.explanation;
  }

  document.getElementById("quiz-progress").textContent =
    `Question ${quizIndex + 1} / ${quizQueue.length} — Score: ${quizScore}`;
  document.getElementById("next-btn").disabled = false;
}

function nextQuestion() {
  quizIndex += 1;
  if (quizIndex >= quizQueue.length) {
    finishQuiz();
  } else {
    renderQuestion();
  }
}

function finishQuiz() {
  stopExamTimer();
  document.getElementById("quiz-panel").style.display = "none";
  document.getElementById("result-panel").style.display = "block";

  const isExam = quizMode === "exam" || quizMode === "exam-short";
  let finalScore = quizScore;
  if (isExam) {
    finalScore = quizQueue.reduce((acc, q, idx) => acc + (userAnswers[idx] === q.correctIndex ? 1 : 0), 0);
  }

  const pct = quizQueue.length ? Math.round((finalScore / quizQueue.length) * 100) : 0;
  const passLabel = isExam ? (pct >= 70 ? " — Admissible (seuil indicatif 70%)" : " — En dessous du seuil indicatif (70%)") : "";
  document.getElementById("result-summary").textContent =
    `${finalScore} / ${quizQueue.length} bonnes réponses (${pct}%)${passLabel}`;

  Storage.recordQuizAttempt({
    date: new Date().toISOString(),
    total: quizQueue.length,
    correct: finalScore,
    mode: quizMode,
  });

  if (isExam) {
    renderReview();
  }
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function renderReview() {
  const container = document.getElementById("result-review");
  container.innerHTML = `<h2 style="margin-top:28px;">Correction détaillée</h2>` + quizQueue.map((q, idx) => {
    const selected = userAnswers[idx];
    const isCorrect = selected === q.correctIndex;
    const selectedText = selected === null ? "(pas de réponse)" : q.options[selected];
    return `
      <div class="review-item ${isCorrect ? "correct" : "incorrect"}">
        <div class="review-q">${idx + 1}. ${escapeHtml(q.question)}</div>
        <div class="review-a">Ta réponse : ${escapeHtml(selectedText)}</div>
        ${!isCorrect ? `<div class="review-correct">Bonne réponse : ${escapeHtml(q.options[q.correctIndex])}</div>` : ""}
        ${q.explanation ? `<div class="explanation">${escapeHtml(q.explanation)}</div>` : ""}
      </div>
    `;
  }).join("");
}

initQuiz();
