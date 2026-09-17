async function main() {
  const session = await requireSession();
  if (!session) return;
  await Storage.init();

  document.getElementById("reset-btn").addEventListener("click", async () => {
    if (!confirm("Réinitialiser toute ta progression (quiz, flashcards, fiches consultées) ? Cette action est irréversible.")) return;
    await Storage.reset();
    location.reload();
  });

  const [modules, questions] = await Promise.all([
    fetch("data/modules.json").then(r => r.json()),
    fetch("data/questions.json").then(r => r.json()),
  ]);

  const state = Storage.getState();
  const questionById = Object.fromEntries(questions.map(q => [q.id, q]));

  const attempts = state.quizAttempts;
  const totalCorrect = attempts.reduce((a, x) => a + x.correct, 0);
  const totalAnswered = attempts.reduce((a, x) => a + x.total, 0);
  const accuracy = totalAnswered ? Math.round((totalCorrect / totalAnswered) * 100) : 0;
  const notesReadCount = Object.keys(state.notesRead).length;
  const examAttempts = attempts.filter(a => a.mode === "exam");
  const bestExam = examAttempts.length
    ? Math.max(...examAttempts.map(a => Math.round((a.correct / a.total) * 100)))
    : null;

  const statsGrid = document.getElementById("stats-grid");
  statsGrid.innerHTML = `
    <div class="card stat-card">
      <div class="stat-value">${questions.length}</div>
      <div class="stat-label">Questions disponibles</div>
    </div>
    <div class="card stat-card">
      <div class="stat-value">${attempts.length}</div>
      <div class="stat-label">Quiz passés</div>
    </div>
    <div class="card stat-card">
      <div class="stat-value">${accuracy}%</div>
      <div class="stat-label">Taux de réussite global</div>
    </div>
    <div class="card stat-card">
      <div class="stat-value">${bestExam !== null ? bestExam + "%" : "—"}</div>
      <div class="stat-label">Meilleur examen blanc</div>
    </div>
    <div class="card stat-card">
      <div class="stat-value">${notesReadCount}/${modules.length}</div>
      <div class="stat-label">Modules consultés</div>
    </div>
  `;

  // Weak-areas breakdown: aggregate per-question accuracy by module (falls back to source if unclassified)
  const moduleById = Object.fromEntries(modules.map(m => [m.slug, m]));
  const byModule = {};
  Object.entries(state.questionStats).forEach(([id, stat]) => {
    const q = questionById[id];
    if (!q || !stat.seen) return;
    const key = q.module || q.source;
    if (!byModule[key]) byModule[key] = { seen: 0, correct: 0 };
    byModule[key].seen += stat.seen;
    byModule[key].correct += stat.correct;
  });
  const moduleRows = Object.entries(byModule)
    .map(([key, s]) => ({
      label: moduleById[key] ? `${String(moduleById[key].id).padStart(2, "0")} — ${moduleById[key].title}` : key,
      pct: Math.round((s.correct / s.seen) * 100),
      seen: s.seen,
    }))
    .sort((a, b) => a.pct - b.pct);

  if (moduleRows.length > 0) {
    document.getElementById("weak-areas-section").style.display = "block";
    document.getElementById("weak-areas-card").innerHTML = moduleRows.map(r => `
      <div style="margin-bottom: 14px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px;">
          <span>${r.label}</span>
          <span class="progress-text" style="margin-top:0;">${r.pct}% (${r.seen} rép.)</span>
        </div>
        <div class="progress-bar"><div style="width:${r.pct}%; background:${r.pct < 60 ? "var(--danger)" : r.pct < 80 ? "var(--warn)" : "var(--accent)"};"></div></div>
      </div>
    `).join("");
  }

  const accuracyByModule = {};
  Object.entries(state.questionStats).forEach(([id, stat]) => {
    const q = questionById[id];
    if (!q || !q.module || !stat.seen) return;
    if (!accuracyByModule[q.module]) accuracyByModule[q.module] = { seen: 0, correct: 0 };
    accuracyByModule[q.module].seen += stat.seen;
    accuracyByModule[q.module].correct += stat.correct;
  });

  const modulesGrid = document.getElementById("modules-grid");
  modulesGrid.innerHTML = modules.map(m => {
    const read = state.notesRead[m.slug];
    const acc = accuracyByModule[m.slug];
    const accBadge = acc ? `<span class="badge ${acc.correct / acc.seen >= 0.8 ? "ready" : "pending"}" style="margin-left:6px;">${Math.round((acc.correct / acc.seen) * 100)}% quiz</span>` : "";
    return `
      <a class="card module-card" href="notes.html?m=${m.slug}">
        <div class="mod-id">MODULE ${String(m.id).padStart(2, "0")}</div>
        <div class="mod-domain">${m.domain}</div>
        <div class="mod-title">${m.title} ${accBadge}</div>
        <div class="progress-bar"><div style="width:${read ? 100 : 0}%"></div></div>
        <div class="progress-text">${read ? "Consulté" : "Pas encore consulté"}</div>
      </a>
    `;
  }).join("");
}
main();
