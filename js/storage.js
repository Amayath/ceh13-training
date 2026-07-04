const Storage = (() => {
  const KEY = "ceh13_progress_v1";

  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return defaultState();
      return { ...defaultState(), ...JSON.parse(raw) };
    } catch (e) {
      return defaultState();
    }
  }

  function defaultState() {
    return {
      quizAttempts: [],       // { date, total, correct, source }
      questionStats: {},      // id -> { seen, correct }
      flashcardStats: {},     // id -> { known: bool, seen }
      notesRead: {},          // moduleSlug -> true
    };
  }

  function save(state) {
    localStorage.setItem(KEY, JSON.stringify(state));
  }

  function recordQuizAttempt(attempt) {
    const state = load();
    state.quizAttempts.push(attempt);
    save(state);
  }

  function recordQuestionResult(id, correct) {
    const state = load();
    const s = state.questionStats[id] || { seen: 0, correct: 0 };
    s.seen += 1;
    if (correct) s.correct += 1;
    state.questionStats[id] = s;
    save(state);
  }

  function recordFlashcard(id, known) {
    const state = load();
    const s = state.flashcardStats[id] || { seen: 0, known: false };
    s.seen += 1;
    s.known = known;
    state.flashcardStats[id] = s;
    save(state);
  }

  function markNotesRead(slug) {
    const state = load();
    state.notesRead[slug] = true;
    save(state);
  }

  function reset() {
    save(defaultState());
  }

  return { load, save, recordQuizAttempt, recordQuestionResult, recordFlashcard, markNotesRead, reset };
})();
