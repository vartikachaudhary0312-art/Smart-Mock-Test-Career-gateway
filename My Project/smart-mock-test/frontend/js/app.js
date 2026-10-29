/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Application Engine & Utilities
 */

document.addEventListener("DOMContentLoaded", () => {
  App.init();
});

const App = {
  init() {
    if (!this.checkAuth()) return;
    this.initTheme();
    this.initHeaderUser();
    this.initGlobalEventListeners();
    this.initBFCacheGuard();
  },

  isPublicPage() {
    const path = window.location.pathname.replace(/\\/g, "/").toLowerCase();
    const filename = path.split("/").pop().split("?")[0] || "index.html";
    const publicPages = ["login.html", "register.html", "index.html", ""];
    return publicPages.includes(filename);
  },

  checkAuth() {
    if (this.isPublicPage()) return true;
    const user = API.getCurrentUser();
    if (!user) {
      window.location.replace(API.getLoginUrl());
      return false;
    }
    const path = window.location.pathname.replace(/\\/g, "/").toLowerCase();
    if (path.includes("/admin/")) {
      const token = localStorage.getItem("smt_auth_token");
      const adminEmail = "vartikachaudhary0312@gmail.com";
      if (!token || user.role !== "admin" || (user.email || "").toLowerCase() !== adminEmail) {
        window.location.replace(API.getLoginUrl());
        return false;
      }
    }
    return true;
  },

  initBFCacheGuard() {
    window.addEventListener("pageshow", (event) => {
      if (event.persisted || (window.performance && window.performance.navigation && window.performance.navigation.type === 2)) {
        if (!App.isPublicPage() && !API.getCurrentUser()) {
          window.location.replace(API.getLoginUrl());
        }
      }
    });
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
    if (!user) return;

    const userElem = document.getElementById("headerUserName");
    const avatarElem = document.getElementById("headerUserAvatar");
    const roleElem = document.getElementById("headerUserRole");
    const emailElem = document.getElementById("headerUserEmail");

    const initials = (user.name || "Student").split(" ").map(n => n[0]).filter(Boolean).join("").substring(0, 2).toUpperCase() || "ST";

    if (userElem) userElem.textContent = user.name;
    if (avatarElem) avatarElem.textContent = initials;
    if (roleElem) roleElem.textContent = (user.role || "student").toUpperCase();
    if (emailElem) emailElem.textContent = user.email || "";

    // Sidebar elements
    const sidebarName = document.getElementById("sidebarUserName");
    const sidebarEmail = document.getElementById("sidebarUserEmail");
    const sidebarAvatar = document.getElementById("sidebarUserAvatar");
    const sidebarRole = document.getElementById("sidebarUserRole");

    if (sidebarName) sidebarName.textContent = user.name;
    if (sidebarEmail) sidebarEmail.textContent = user.email || "";
    if (sidebarAvatar) sidebarAvatar.textContent = initials;
    if (sidebarRole) sidebarRole.textContent = (user.role || "student").toUpperCase();

    // Welcome banner text
    const welcomeElem = document.getElementById("dashboardWelcomeText");
    if (welcomeElem) {
      welcomeElem.textContent = `Welcome back, ${user.name} 👋`;
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
