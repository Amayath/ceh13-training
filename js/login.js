let mode = "login";

const tabLogin = document.getElementById("tab-login");
const tabSignup = document.getElementById("tab-signup");
const form = document.getElementById("auth-form");
const errorBox = document.getElementById("auth-error");
const successBox = document.getElementById("auth-success");
const submitBtn = document.getElementById("submit-btn");
const passwordField = document.getElementById("password-field");
const passwordInput = document.getElementById("password");
const forgotToggle = document.getElementById("forgot-toggle");

function setMode(m) {
  mode = m;
  errorBox.style.display = "none";
  successBox.style.display = "none";

  tabLogin.classList.toggle("active", m === "login");
  tabSignup.classList.toggle("active", m === "signup");

  if (m === "forgot") {
    passwordField.style.display = "none";
    passwordInput.required = false;
    submitBtn.textContent = "Envoyer le lien de réinitialisation";
  } else {
    passwordField.style.display = "block";
    passwordInput.required = true;
    submitBtn.textContent = m === "login" ? "Se connecter" : "Créer mon compte";
  }
}

tabLogin.addEventListener("click", () => setMode("login"));
tabSignup.addEventListener("click", () => setMode("signup"));
forgotToggle.addEventListener("click", (e) => {
  e.preventDefault();
  setMode("forgot");
});

function translateError(msg) {
  if (/already registered|already exists/i.test(msg)) return "Un compte existe déjà avec cet email. Essaie de te connecter.";
  if (/invalid login credentials/i.test(msg)) return "Email ou mot de passe incorrect.";
  if (/password.*(least|short)/i.test(msg)) return "Le mot de passe doit faire au moins 8 caractères.";
  if (/rate limit/i.test(msg)) return "Trop de tentatives, réessaie dans quelques instants.";
  if (/failed to fetch|networkerror|load failed/i.test(msg)) return "Impossible de contacter le serveur. Le service est peut-être en pause — réessaie dans une minute ou préviens Amaya.";
  return msg;
}

(async () => {
  try {
    const { data: { session } } = await sbClient.auth.getSession();
    if (session) window.location.href = "index.html";
  } catch (e) {
    /* network issue on initial check — let the user try to log in, which will surface a clear error */
  }
})();

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorBox.style.display = "none";
  successBox.style.display = "none";
  submitBtn.disabled = true;

  const email = document.getElementById("email").value.trim();
  const password = passwordInput.value;

  try {
    if (mode === "forgot") {
      const { error } = await sbClient.auth.resetPasswordForEmail(email, {
        redirectTo: new URL("reset-password.html", window.location.href).toString(),
      });
      if (error) throw error;
      successBox.textContent = "Si un compte existe avec cet email, un lien de réinitialisation vient d'être envoyé.";
      successBox.style.display = "block";
      submitBtn.disabled = false;
      return;
    }

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
