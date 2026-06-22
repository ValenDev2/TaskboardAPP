// board.js - Logica del tablero de tareas
//
// Permisos de movimiento:
//   Owner  - puede arrastrar a cualquier columna
//   Member - puede arrastrar a "in_progress" o "in_review"
//            NO puede mover a "backlog" (para atras) ni a "done" (decide el owner)

if (!Api.getToken()) {
  window.location.href = "index.html";
}

const params = new URLSearchParams(window.location.search);
const PROJECT_ID = params.get("project");

const COLUMNS = [
  { status: "backlog",     label: "Backlog" },
  { status: "in_progress", label: "En curso" },
  { status: "in_review",   label: "En revision" },
  { status: "done",        label: "Hecho" },
];

// Estados a los que un member puede mover tareas
const MEMBER_ALLOWED = ["in_progress", "in_review"];

let currentUserRole = null;
let allTasks = [];

function showError(message) {
  const box = document.getElementById("error-box");
  box.textContent = message;
  box.classList.add("visible");
  setTimeout(() => box.classList.remove("visible"), 4000);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function logout() {
  Api.clearToken();
  window.location.href = "index.html";
}

function renderColumns() {
  const board = document.getElementById("board");
  board.innerHTML = COLUMNS.map((col) => `
    <div class="column">
      <div class="column-head">
        <span>${col.label}</span>
        <span class="column-count" id="count-${col.status}">0</span>
      </div>
      <div class="column-body" id="col-${col.status}"
           ondragover="handleDragOver(event)"
           ondrop="handleDrop(event, '${col.status}')">
      </div>
      ${col.status === "backlog" && currentUserRole === "owner" ? `
        <button class="btn btn-ghost btn-small add-task-btn" onclick="toggleNewTaskForm()">
          + Nueva tarea
        </button>
      ` : ""}
    </div>
  `).join("");
}

function renderTasks() {
  COLUMNS.forEach((col) => {
    const container = document.getElementById(`col-${col.status}`);
    const tasksInColumn = allTasks.filter((t) => t.status === col.status);

    document.getElementById(`count-${col.status}`).textContent = tasksInColumn.length;

    if (tasksInColumn.length === 0) {
      container.innerHTML = `<div class="column-empty">Sin tareas</div>`;
      return;
    }

    container.innerHTML = tasksInColumn.map((task) => `
      <div class="task-card"
           draggable="true"
           ondragstart="handleDragStart(event, ${task.id})">
        <p class="task-title">${escapeHtml(task.title)}</p>
        ${task.description ? `<p class="task-desc">${escapeHtml(task.description)}</p>` : ""}
        <div class="task-footer">
          ${currentUserRole === "owner" ? `
            <button class="task-delete" onclick="handleDeleteTask(event, ${task.id})" title="Eliminar">x</button>
          ` : ""}
        </div>
      </div>
    `).join("");
  });
}

//Drag and drop
let draggedTaskId = null;

function handleDragStart(event, taskId) {
  draggedTaskId = taskId;
  event.dataTransfer.effectAllowed = "move";
}

function handleDragOver(event) {
  event.preventDefault();
}

async function handleDrop(event, newStatus) {
  event.preventDefault();
  if (draggedTaskId === null) return;

  const task = allTasks.find((t) => t.id === draggedTaskId);
  if (!task || task.status === newStatus) return;

  // Validacion en el frontend (el backend tambien valida)
  if (currentUserRole !== "owner" && !MEMBER_ALLOWED.includes(newStatus)) {
    showError("Solo podés mover tareas a 'En curso' o 'En revision'");
    draggedTaskId = null;
    return;
  }

  try {
    await Api.updateTaskStatus(draggedTaskId, newStatus);
    task.status = newStatus;
    renderTasks();
  } catch (err) {
    showError(err.message);
  }

  draggedTaskId = null;
}

// -- Crear tarea --
function toggleNewTaskForm() {
  document.getElementById("new-task-modal").classList.toggle("hidden");
}

async function handleCreateTask(event) {
  event.preventDefault();
  const title = document.getElementById("new-task-title").value;
  const description = document.getElementById("new-task-desc").value;

  try {
    const task = await Api.createTask(PROJECT_ID, title, description || null, "backlog");
    allTasks.push(task);
    renderTasks();
    document.getElementById("new-task-title").value = "";
    document.getElementById("new-task-desc").value = "";
    toggleNewTaskForm();
  } catch (err) {
    showError(err.message);
  }
}

// -- Eliminar tarea --
async function handleDeleteTask(event, taskId) {
  event.stopPropagation();
  if (!confirm("Eliminar esta tarea? Esta accion no se puede deshacer.")) return;

  try {
    await Api.deleteTask(taskId);
    allTasks = allTasks.filter((t) => t.id !== taskId);
    renderTasks();
  } catch (err) {
    showError(err.message);
  }
}

//Invitaciones
async function handleInvite() {
  try {
    const invitation = await Api.createInvitation(PROJECT_ID);
    document.getElementById("invite-code-box").textContent = invitation.code;
    document.getElementById("invite-result").classList.remove("hidden");
  } catch (err) {
    showError(err.message);
  }
}

function copyInviteCode() {
  const code = document.getElementById("invite-code-box").textContent;
  navigator.clipboard.writeText(code);
}

//Carga inicial
async function loadBoard() {
  try {
    const [project, user, tasks] = await Promise.all([
      Api.request(`/projects/${PROJECT_ID}`),
      Api.getMe(),
      Api.listTasks(PROJECT_ID),
    ]);

    currentUserRole = project.my_role;
    allTasks = tasks;

    document.getElementById("project-title").textContent = project.name;
    document.getElementById("user-label").textContent = user.username;

    if (currentUserRole === "owner") {
      document.getElementById("invite-btn").classList.remove("hidden");
    }

    renderColumns();
    renderTasks();
  } catch (err) {
    showError(err.message);
  }
}

loadBoard();