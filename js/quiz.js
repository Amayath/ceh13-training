let ALL_QUESTIONS = [];
let quizQueue = [];
let quizIndex = 0;
let quizScore = 0;
let quizAnswered = false;

async function initQuiz() {
  ALL_QUESTIONS = await fetch("data/questions.json").then(r => r.json());
  const sources = [...new Set(ALL_QUESTIONS.map(q => q.source))].sort();
  const select = document.getElementById("source-select");
  sources.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s;
    opt.textContent = `${s} (${ALL_QUESTIONS.filter(q => q.source === s).length})`;
    select.appendChild(opt);
  });

  document.getElementById("start-btn").addEventListener("click", startQuiz);
  document.getElementById("next-btn").addEventListener("click", nextQuestion);
  document.getElementById("quit-btn").addEventListener("click", () => location.reload());
  document.getElementById("restart-btn").addEventListener("click", () => location.reload());
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function startQuiz() {
  const source = document.getElementById("source-select").value;
  const count = parseInt(document.getElementById("count-input").value, 10) || 20;
  const doShuffle = document.getElementById("shuffle-check").checked;

  let pool = source === "all" ? ALL_QUESTIONS : ALL_QUESTIONS.filter(q => q.source === source);
  pool = doShuffle ? shuffle(pool) : pool;
  quizQueue = pool.slice(0, Math.min(count, pool.length));
  quizIndex = 0;
  quizScore = 0;

  document.getElementById("setup-panel").style.display = "none";
  document.getElementById("result-panel").style.display = "none";
  document.getElementById("quiz-panel").style.display = "block";
  renderQuestion();
}

function renderQuestion() {
  quizAnswered = false;
  const q = quizQueue[quizIndex];
  document.getElementById("quiz-progress").textContent = `Question ${quizIndex + 1} / ${quizQueue.length} — Score: ${quizScore}`;
  document.getElementById("q-source").textContent = q.source;
  document.getElementById("q-text").textContent = q.question;
  document.getElementById("q-explanation").style.display = "none";
  document.getElementById("q-explanation").textContent = "";
  document.getElementById("next-btn").disabled = true;

  const optsWrap = document.getElementById("q-options");
  optsWrap.innerHTML = "";
  q.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "option";
    btn.textContent = opt;
    btn.addEventListener("click", () => selectAnswer(i));
    optsWrap.appendChild(btn);
  });
}

function selectAnswer(i) {
  if (quizAnswered) return;
  quizAnswered = true;
  const q = quizQueue[quizIndex];
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

  document.getElementById("quiz-progress").textContent = `Question ${quizIndex + 1} / ${quizQueue.length} — Score: ${quizScore}`;
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
  document.getElementById("quiz-panel").style.display = "none";
  document.getElementById("result-panel").style.display = "block";
  const pct = Math.round((quizScore / quizQueue.length) * 100);
  document.getElementById("result-summary").textContent =
    `${quizScore} / ${quizQueue.length} bonnes réponses (${pct}%)`;
  Storage.recordQuizAttempt({
    date: new Date().toISOString(),
    total: quizQueue.length,
    correct: quizScore,
  });
}

initQuiz();
