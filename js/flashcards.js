let ALL_CARDS = [];
let MODULES = [];
let deck = [];
let cardIndex = 0;
let flipped = false;

async function initFlashcards() {
  const [cards, modules] = await Promise.all([
    fetch("data/flashcards.json").then(r => r.json()),
    fetch("data/modules.json").then(r => r.json()),
  ]);
  ALL_CARDS = cards;
  MODULES = modules;

  const moduleSelect = document.getElementById("module-select");
  const modulesWithCards = modules.filter(m => cards.some(c => c.module === m.slug));
  modulesWithCards.forEach(m => {
    const opt = document.createElement("option");
    opt.value = m.slug;
    opt.textContent = `${String(m.id).padStart(2, "0")} — ${m.title}`;
    moduleSelect.appendChild(opt);
  });

  moduleSelect.addEventListener("change", buildDeck);
  document.getElementById("unknown-only-check").addEventListener("change", buildDeck);
  document.getElementById("fc-card").addEventListener("click", flipCard);
  document.getElementById("fc-next").addEventListener("click", () => moveCard(1));
  document.getElementById("fc-prev").addEventListener("click", () => moveCard(-1));
  document.getElementById("fc-known").addEventListener("click", () => markCard(true));
  document.getElementById("fc-unknown").addEventListener("click", () => markCard(false));

  buildDeck();
}

function buildDeck() {
  const moduleFilter = document.getElementById("module-select").value;
  const unknownOnly = document.getElementById("unknown-only-check").checked;
  const state = Storage.load();

  deck = ALL_CARDS.filter(c => moduleFilter === "all" || c.module === moduleFilter);
  if (unknownOnly) {
    deck = deck.filter(c => !(state.flashcardStats[c.id] && state.flashcardStats[c.id].known));
  }
  cardIndex = 0;
  flipped = false;

  const wrap = document.getElementById("fc-wrap");
  const empty = document.getElementById("empty-state");
  if (deck.length === 0) {
    wrap.style.display = "none";
    empty.style.display = "block";
    return;
  }
  wrap.style.display = "flex";
  empty.style.display = "none";
  renderCard();
}

function renderCard() {
  flipped = false;
  const card = deck[cardIndex];
  const state = Storage.load();
  const stat = state.flashcardStats[card.id];
  const knownTag = stat && stat.known ? " · connue" : "";
  document.getElementById("fc-progress").textContent =
    `Carte ${cardIndex + 1} / ${deck.length}${knownTag}`;
  const el = document.getElementById("fc-card");
  el.className = "flashcard";
  el.textContent = card.front;
}

function flipCard() {
  flipped = !flipped;
  const card = deck[cardIndex];
  const el = document.getElementById("fc-card");
  if (flipped) {
    el.textContent = card.back;
    el.classList.add("back");
  } else {
    el.textContent = card.front;
    el.classList.remove("back");
  }
}

function moveCard(delta) {
  cardIndex = (cardIndex + delta + deck.length) % deck.length;
  renderCard();
}

function markCard(known) {
  const card = deck[cardIndex];
  Storage.recordFlashcard(card.id, known);
  moveCard(1);
}

initFlashcards();
