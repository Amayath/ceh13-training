const Storage = (() => {
  const KEY = "ceh13_progress_v1";
  let cachedState = null;

  function defaultState() {
    return {
      quizAttempts: [],       // { date, total, correct, source, mode }
      questionStats: {},      // id -> { seen, correct, lastCorrect }
      flashcardStats: {},     // id -> { known: bool, seen }
      notesRead: {},          // moduleSlug -> true
    };
  }

  async function init() {
    try {
      const raw = localStorage.getItem(KEY);
      cachedState = raw ? { ...defaultState(), ...JSON.parse(raw) } : defaultState();
    } catch (e) {
      cachedState = defaultState();
    }
    return cachedState;
  }

  function getState() {
    return cachedState || defaultState();
  }

  function persist() {
    try {
      localStorage.setItem(KEY, JSON.stringify(cachedState));
    } catch (e) {
      /* storage unavailable, ignore */
    }
  }

  function recordQuizAttempt(attempt) {
    cachedState.quizAttempts.push(attempt);
    persist();
  }

  function recordQuestionResult(id, correct) {
    const s = cachedState.questionStats[id] || { seen: 0, correct: 0 };
    s.seen += 1;
    if (correct) s.correct += 1;
    s.lastCorrect = correct;
    cachedState.questionStats[id] = s;
    persist();
  }

  function recordFlashcard(id, known) {
    const s = cachedState.flashcardStats[id] || { seen: 0, known: false };
    s.seen += 1;
    s.known = known;
    cachedState.flashcardStats[id] = s;
    persist();
  }

  function markNotesRead(slug) {
    cachedState.notesRead[slug] = true;
    persist();
  }

  function reset() {
    cachedState = defaultState();
    persist();
  }

  return { init, getState, recordQuizAttempt, recordQuestionResult, recordFlashcard, markNotesRead, reset };
})();
