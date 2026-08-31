let mode = "login";

const tabLogin = document.getElementById("tab-login");
const tabSignup = document.getElementById("tab-signup");
const form = document.getElementById("auth-form");
const errorBox = document.getElementById("auth-error");
const submitBtn = document.getElementById("submit-btn");

function setMode(m) {
  mode = m;
  tabLogin.classList.toggle("active", m === "login");
  tabSignup.classList.toggle("active", m === "signup");
  submitBtn.textContent = m === "login" ? "Se connecter" : "Créer mon compte";
  errorBox.style.display = "none";
}

tabLogin.addEventListener("click", () => setMode("login"));
tabSignup.addEventListener("click", () => setMode("signup"));

function translateError(msg) {
  if (/already registered|already exists/i.test(msg)) return "Un compte existe déjà avec cet email. Essaie de te connecter.";
  if (/invalid login credentials/i.test(msg)) return "Email ou mot de passe incorrect.";
  if (/password.*(least|short)/i.test(msg)) return "Le mot de passe doit faire au moins 6 caractères.";
  if (/rate limit/i.test(msg)) return "Trop de tentatives, réessaie dans quelques instants.";
  return msg;
}

(async () => {
  const { data: { session } } = await sbClient.auth.getSession();
  if (session) window.location.href = "index.html";
})();

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorBox.style.display = "none";
  submitBtn.disabled = true;

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    if (mode === "signup") {
      const { error } = await sbClient.auth.signUp({ email, password });
      if (error) throw error;
    } else {
      const { error } = await sbClient.auth.signInWithPassword({ email, password });
      if (error) throw error;
    }
    window.location.href = "index.html";
  } catch (err) {
    errorBox.textContent = translateError(err.message || String(err));
    errorBox.style.display = "block";
    submitBtn.disabled = false;
  }
});
