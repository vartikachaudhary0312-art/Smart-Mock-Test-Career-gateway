/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Navigation & Collapsible Sidebar Drawer Handler
 * Clean collapsible drawer navigation for the Student Portal across all screen sizes
 */

document.addEventListener("DOMContentLoaded", () => {
  Navigation.init();
});

const Navigation = {
  sidebar: null,
  toggleBtn: null,
  closeBtn: null,
  backdrop: null,
  isInitialized: false,

  init() {
    this.sidebar = document.querySelector(".app-sidebar");
    this.toggleBtn = document.querySelector(".mobile-nav-toggle, #btnSidebarToggle");
    this.createBackdrop();
    this.bindEvents();
    this.highlightActiveRoute();
    this.closeSidebar(); // Ensure hidden default state on initial load
    this.isInitialized = true;
  },

  createBackdrop() {
    let backdrop = document.querySelector(".sidebar-backdrop");
    if (!backdrop) {
      backdrop = document.createElement("div");
      backdrop.className = "sidebar-backdrop";
      backdrop.setAttribute("tabindex", "-1");
      backdrop.setAttribute("aria-hidden", "true");
      document.body.appendChild(backdrop);
    }
    this.backdrop = backdrop;
  },

  bindEvents() {
    // 1. Hamburger Toggle Button
    if (this.toggleBtn) {
      this.toggleBtn.setAttribute("aria-label", "Toggle Navigation Menu");
      this.toggleBtn.setAttribute("aria-expanded", "false");
      this.toggleBtn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.toggleSidebar();
      });
    }

    // 2. Sidebar Header Close Button
    this.closeBtn = document.querySelector(".sidebar-close-btn");
    if (this.closeBtn) {
      this.closeBtn.addEventListener("click", (e) => {
        e.preventDefault();
        this.closeSidebar();
        this.toggleBtn?.focus();
      });
    }

    // 3. Subtle Backdrop Overlay Click
    if (this.backdrop) {
      this.backdrop.addEventListener("click", () => this.closeSidebar());
    }

    // 4. Outside Click Listener
    document.addEventListener("click", (e) => {
      if (this.isOpen()) {
        const clickedInsideSidebar = this.sidebar && this.sidebar.contains(e.target);
        const clickedToggle = this.toggleBtn && this.toggleBtn.contains(e.target);
        if (!clickedInsideSidebar && !clickedToggle) {
          this.closeSidebar();
        }
      }
    });

    // 5. Escape Key Listener
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.isOpen()) {
        this.closeSidebar();
        this.toggleBtn?.focus();
      }
    });

    // 6. Navigation Item Click: Automatically Close Navbar Immediately
    const navLinks = document.querySelectorAll(".nav-link-custom");
    navLinks.forEach(link => {
      link.addEventListener("click", () => {
        this.closeSidebar();
      });
    });

    // 7. Ensure closed state on browser back/forward and view switches
    window.addEventListener("pageshow", () => {
      this.closeSidebar();
      this.highlightActiveRoute();
    });

    window.addEventListener("popstate", () => {
      this.closeSidebar();
      this.highlightActiveRoute();
    });
  },

  isOpen() {
    return Boolean(this.sidebar && this.sidebar.classList.contains("show"));
  },

  toggleSidebar() {
    if (this.isOpen()) {
      this.closeSidebar();
    } else {
      this.openSidebar();
    }
  },

  openSidebar() {
    if (this.sidebar) {
      this.sidebar.classList.add("show");
      if (this.backdrop) this.backdrop.classList.add("show");
      document.body.style.overflow = "hidden";
      if (this.toggleBtn) this.toggleBtn.setAttribute("aria-expanded", "true");
    }
  },

  closeSidebar() {
    if (this.sidebar) {
      this.sidebar.classList.remove("show");
      if (this.backdrop) this.backdrop.classList.remove("show");
      document.body.style.overflow = "";
      if (this.toggleBtn) this.toggleBtn.setAttribute("aria-expanded", "false");
    }
  },

  highlightActiveRoute() {
    const rawPath = window.location.pathname.replace(/\\/g, "/");
    let currentFile = rawPath.split("/").pop().split("?")[0].split("#")[0] || "student-dashboard.html";
    if (currentFile === "" || currentFile === "index.html") {
      currentFile = "student-dashboard.html";
    }

    const navLinks = document.querySelectorAll(".nav-link-custom");
    navLinks.forEach(link => {
      const href = (link.getAttribute("href") || "").split("?")[0].split("#")[0];
      if (href && (href === currentFile || href.endsWith("/" + currentFile))) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
      } else {
        link.classList.remove("active");
        link.removeAttribute("aria-current");
      }
    });
  }
};
