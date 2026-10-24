/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Application Engine & Utilities
 */

document.addEventListener("DOMContentLoaded", () => {
  App.init();
});

const App = {
  init() {
    this.initTheme();
    this.initHeaderUser();
    this.initGlobalEventListeners();
  },

  initTheme() {
    const savedTheme = localStorage.getItem("smt_theme") || "light";
    this.setTheme(savedTheme);

    const themeToggleBtns = document.querySelectorAll(".theme-toggle-btn");
    themeToggleBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        const current = document.documentElement.getAttribute("data-bs-theme") || "light";
        const next = current === "light" ? "dark" : "light";
        this.setTheme(next);
      });
    });
  },

  setTheme(theme) {
    document.documentElement.setAttribute("data-bs-theme", theme);
    if (theme === "dark") {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
    localStorage.setItem("smt_theme", theme);

    // Update icon visually
    const icons = document.querySelectorAll(".theme-toggle-btn i");
    icons.forEach(icon => {
      icon.className = theme === "dark" ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
    });

    // Re-render charts if active
    if (window.ChartManager && typeof window.ChartManager.updateTheme === "function") {
      window.ChartManager.updateTheme(theme);
    }
  },

  initHeaderUser() {
    const user = API.getCurrentUser();
    const userElem = document.getElementById("headerUserName");
    const avatarElem = document.getElementById("headerUserAvatar");
    const roleElem = document.getElementById("headerUserRole");

    if (userElem && user) {
      userElem.textContent = user.name;
    }
    if (avatarElem && user) {
      const initials = user.name.split(" ").map(n => n[0]).join("").substring(0, 2).toUpperCase();
      avatarElem.textContent = initials;
    }
    if (roleElem && user) {
      roleElem.textContent = user.role.toUpperCase();
    }
  },

  initGlobalEventListeners() {
    // Logout handlers
    const logoutBtns = document.querySelectorAll(".action-logout");
    logoutBtns.forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        API.logout();
      });
    });
  },

  showToast(message, type = "success") {
    let container = document.querySelector(".toast-container-custom");
    if (!container) {
      container = document.createElement("div");
      container.className = "toast-container-custom";
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast-custom toast-${type}`;
    
    let iconClass = "bi-check-circle-fill text-success";
    if (type === "error") iconClass = "bi-exclamation-octagon-fill text-danger";
    if (type === "warning") iconClass = "bi-exclamation-triangle-fill text-warning";

    toast.innerHTML = `
      <i class="bi ${iconClass} fs-5"></i>
      <div class="flex-grow-1">
        <div class="fw-semibold text-capitalize">${type}</div>
        <div class="small opacity-90">${message}</div>
      </div>
      <button type="button" class="btn-close ms-2" onclick="this.parentElement.remove()"></button>
    `;

    container.appendChild(toast);
    setTimeout(() => {
      if (toast.parentElement) toast.remove();
    }, 4000);
  }
};
