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

  function loadLocal() {
    try {
      const raw = localStorage.getItem(KEY);
      return raw ? { ...defaultState(), ...JSON.parse(raw) } : defaultState();
    } catch (e) {
      return defaultState();
    }
  }

  function saveLocal() {
    try {
      localStorage.setItem(KEY, JSON.stringify(cachedState));
    } catch (e) {
      /* storage unavailable, ignore */
    }
  }

  async function init() {
    const local = loadLocal();
    const { data: { session } } = await sbClient.auth.getSession();
    if (!session) {
      cachedState = local;
      return cachedState;
    }

    try {
      const { data, error } = await sbClient
        .from("user_progress")
        .select("data")
        .eq("user_id", session.user.id)
        .maybeSingle();
      cachedState = !error && data && data.data ? { ...defaultState(), ...data.data } : local;
    } catch (e) {
      cachedState = local;
    }
    return cachedState;
  }

  function getState() {
    return cachedState || defaultState();
  }

  async function persistRemote() {
    const { data: { session } } = await sbClient.auth.getSession();
    if (!session) return;
    await sbClient.from("user_progress").upsert({
      user_id: session.user.id,
      data: cachedState,
      updated_at: new Date().toISOString(),
    });
  }

  function persist() {
    saveLocal();
    persistRemote();
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
