async function requireSession() {
  let session = null;
  try {
    const result = await Promise.race([
      sbClient.auth.getSession(),
      new Promise((_, reject) => setTimeout(() => reject(new Error("timeout")), 10000)),
    ]);
    session = result.data.session;
  } catch (e) {
    showServiceUnavailable();
    return null;
  }

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

function showServiceUnavailable() {
  const container = document.querySelector(".container") || document.body;
  container.innerHTML = `
    <div class="empty-state" style="padding-top:80px;">
      <p style="font-size:16px; color:var(--text); margin-bottom:8px;">Service momentanément indisponible</p>
      <p>Impossible de contacter le serveur de comptes. Il est peut-être en pause — réessaie dans une minute.</p>
      <button class="btn secondary small" style="margin-top:16px;" onclick="location.reload()">Réessayer</button>
    </div>
  `;
}
