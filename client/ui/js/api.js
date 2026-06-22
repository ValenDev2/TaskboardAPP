// api.js — comunicacion con backend

const API_URL = "http://localhost:8000";

const Api = {
  /** Devuelve el token guardado, o null si no hay sesión. */
  getToken() {
    return localStorage.getItem("token");
  },

  /** Guarda el token después del login/registro. */
  setToken(token) {
    localStorage.setItem("token", token);
  },

  /** Borra la sesión (logout). */
  clearToken() {
    localStorage.removeItem("token");
  },

  /**
   * Hace un request al backend agregando el header de autenticación
   * automáticamente si hay un token guardado.
   *
   * @param {string} path
   * @param {object} options
   */
  async request(path, options = {}) {
    const headers = { "Content-Type": "application/json", ...options.headers };
    const token = this.getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const response = await fetch(`${API_URL}${path}`, { ...options, headers });

    const data = response.status === 204 ? null : await response.json();

    if (!response.ok) {
      const message = data?.detail || "Ocurrió un error inesperado";
      throw new Error(typeof message === "string" ? message : JSON.stringify(message));
    }

    return data;
  },

  // Auth
  register(username, email, password) {
    return this.request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
    });
  },

  login(email, password) {
    return this.request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  },

  getMe() {
    return this.request("/auth/me");
  },

  // Proyectos
  listProjects() {
    return this.request("/projects");
  },

  createProject(name, description) {
    return this.request("/projects", {
      method: "POST",
      body: JSON.stringify({ name, description }),
    });
  },

  joinProject(code) {
    return this.request("/projects/join", {
      method: "POST",
      body: JSON.stringify({ code }),
    });
  },

  createInvitation(projectId) {
    return this.request(`/projects/${projectId}/invite`, { method: "POST" });
  },

  // Tareas
  listTasks(projectId) {
    return this.request(`/projects/${projectId}/tasks`);
  },

  createTask(projectId, title, description, status = "backlog") {
    return this.request(`/projects/${projectId}/tasks`, {
      method: "POST",
      body: JSON.stringify({ title, description, status }),
    });
  },

  updateTaskStatus(taskId, status) {
    return this.request(`/tasks/${taskId}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
  },

  deleteTask(taskId) {
    return this.request(`/tasks/${taskId}`, { method: "DELETE" });
  },
};