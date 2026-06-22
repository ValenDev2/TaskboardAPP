// dashboard.js — Lógica de la pantalla de "Mis proyectos"

// Si no hay sesión, mandar de vuelta al login
if (!Api.getToken()) {
  window.location.href = "index.html";
}

function logout() {
  Api.clearToken();
  window.location.href = "index.html";
}

function showError(message) {
  const box = document.getElementById("error-box");
  box.textContent = message;
  box.classList.add("visible");
}

function toggleForm(id) {
  const forms = ["create-form", "join-form"];
  forms.forEach((formId) => {
    const el = document.getElementById(formId);
    if (formId === id) el.classList.toggle("hidden");
    else el.classList.add("hidden");
  });
}

function renderProjects(projects) {
  const list = document.getElementById("project-list");

  if (projects.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        Todavía no tenés proyectos.<br/>
        Creá uno nuevo o unite con un código de invitación.
      </div>`;
    return;
  }

  list.innerHTML = projects.map((p) => `
    <div class="project-card" onclick="openProject(${p.id})">
      <div>
        <h3>${escapeHtml(p.name)}</h3>
        <p class="muted">${escapeHtml(p.description || "Sin descripción")}</p>
      </div>
      <span class="role-badge ${p.my_role === "owner" ? "role-owner" : "role-member"}">
        ${p.my_role === "owner" ? "Creador" : "Miembro"}
      </span>
    </div>
  `).join("");
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function openProject(projectId) {
  window.location.href = `board.html?project=${projectId}`;
}

async function loadProjects() {
  try {
    const projects = await Api.listProjects();
    renderProjects(projects);
  } catch (err) {
    showError(err.message);
  }
}

async function handleCreateProject(event) {
  event.preventDefault();
  const name = document.getElementById("new-project-name").value;

  try {
    await Api.createProject(name, null);
    document.getElementById("new-project-name").value = "";
    toggleForm("create-form"); // cerrar el formulario
    loadProjects();
  } catch (err) {
    showError(err.message);
  }
}

async function handleJoinProject(event) {
  event.preventDefault();
  const code = document.getElementById("join-code").value;

  try {
    await Api.joinProject(code);
    document.getElementById("join-code").value = "";
    toggleForm("join-form");
    loadProjects();
  } catch (err) {
    showError(err.message);
  }
}

/** Muestra el nombre de usuario en la barra superior. */
async function loadUser() {
  try {
    const user = await Api.getMe();
    document.getElementById("user-label").textContent = user.username;
  } catch {
    logout(); // si el token expiró o es inválido, manda al login
  }
}

loadUser();
loadProjects();