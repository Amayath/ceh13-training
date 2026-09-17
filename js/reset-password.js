const form = document.getElementById("reset-form");
const errorBox = document.getElementById("reset-error");
const successBox = document.getElementById("reset-success");
const submitBtn = document.getElementById("reset-submit-btn");

// Supabase sends the recovery token in the URL hash; the client picks it up
// automatically and fires a PASSWORD_RECOVERY auth event once ready.
sbClient.auth.onAuthStateChange((event) => {
  if (event === "PASSWORD_RECOVERY") {
    errorBox.style.display = "none";
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorBox.style.display = "none";
  successBox.style.display = "none";
  submitBtn.disabled = true;

  const newPassword = document.getElementById("new-password").value;
  const { error } = await sbClient.auth.updateUser({ password: newPassword });

  if (error) {
    errorBox.textContent = error.message;
    errorBox.style.display = "block";
    submitBtn.disabled = false;
    return;
  }

  successBox.textContent = "Mot de passe mis à jour. Redirection...";
  successBox.style.display = "block";
  setTimeout(() => { window.location.href = "index.html"; }, 1500);
});
