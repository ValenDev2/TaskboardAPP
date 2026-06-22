// auth.js — Lógica de la pantalla de login/registro

/** Cambia entre el tab de "Iniciar sesión" y "Crear cuenta". */
function switchTab(tab) {
  const isLogin = tab === "login";

  document.getElementById("tab-login").classList.toggle("active", isLogin);
  document.getElementById("tab-register").classList.toggle("active", !isLogin);
  document.getElementById("form-login").style.display = isLogin ? "block" : "none";
  document.getElementById("form-register").style.display = isLogin ? "none" : "block";

  hideError();
}

function showError(message) {
  const box = document.getElementById("error-box");
  box.textContent = message;
  box.classList.add("visible");
}

function hideError() {
  document.getElementById("error-box").classList.remove("visible");
}

/** Al loguearse o registrarse con éxito, guarda el token y entra al dashboard. */
function goToDashboard(token) {
  Api.setToken(token);
  window.location.href = "dashboard.html";
}

async function handleLogin(event) {
  event.preventDefault();
  hideError();

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  try {
    const data = await Api.login(email, password);
    goToDashboard(data.access_token);
  } catch (err) {
    showError(err.message);
  }
}

async function handleRegister(event) {
  event.preventDefault();
  hideError();

  const username = document.getElementById("reg-username").value;
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;

  try {
    const data = await Api.register(username, email, password);
    goToDashboard(data.access_token);
  } catch (err) {
    showError(err.message);
  }
}

// Si ya hay una sesión guardada, saltar directo al dashboard
if (Api.getToken()) {
  window.location.href = "dashboard.html";
}