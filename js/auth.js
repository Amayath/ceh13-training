async function requireSession() {
  const { data: { session } } = await sbClient.auth.getSession();
  if (!session) {
    window.location.href = "login.html";
    return null;
  }

  const emailEl = document.getElementById("user-email");
  if (emailEl) emailEl.textContent = session.user.email;

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      await sbClient.auth.signOut();
      window.location.href = "login.html";
    });
  }

  return session;
}
