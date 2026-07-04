let MODULES = [];
let NOTES = {};

function getParam(name) {
  return new URLSearchParams(location.search).get(name);
}

async function initNotes() {
  const [modules, notes] = await Promise.all([
    fetch("data/modules.json").then(r => r.json()),
    fetch("data/notes.json").then(r => r.json()),
  ]);
  MODULES = modules;
  NOTES = notes;

  const toc = document.getElementById("notes-toc");
  toc.innerHTML = modules.map(m => {
    const ready = !!notes[m.slug];
    return `<a href="notes.html?m=${m.slug}" data-slug="${m.slug}">
      ${String(m.id).padStart(2, "0")}. ${m.title}
      <span class="badge ${ready ? "ready" : "pending"}" style="margin-left:6px;">${ready ? "prêt" : "à venir"}</span>
    </a>`;
  }).join("");

  toc.querySelectorAll("a").forEach(a => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      history.pushState(null, "", `notes.html?m=${a.dataset.slug}`);
      renderModule(a.dataset.slug);
    });
  });

  const initialSlug = getParam("m") || modules[0].slug;
  renderModule(initialSlug);
}

function renderModule(slug) {
  document.querySelectorAll(".notes-toc a").forEach(a => {
    a.classList.toggle("active", a.dataset.slug === slug);
  });

  const module = MODULES.find(m => m.slug === slug);
  const content = document.getElementById("notes-content");
  const noteData = NOTES[slug];

  if (!noteData) {
    content.innerHTML = `
      <div class="empty-state">
        Les fiches de cours pour <strong>${module ? module.title : slug}</strong> arrivent bientôt.
      </div>
    `;
    return;
  }

  Storage.markNotesRead(slug);

  content.innerHTML = noteData.sections.map(sec => `
    <h3>${sec.heading}</h3>
    ${sec.html}
  `).join("");
}

initNotes();
