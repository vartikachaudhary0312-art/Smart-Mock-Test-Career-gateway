/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Navigation & Responsive Mobile Sidebar Drawer Handler
 */

document.addEventListener("DOMContentLoaded", () => {
  Navigation.init();
});

const Navigation = {
  init() {
    this.sidebar = document.querySelector(".app-sidebar");
    this.toggleBtn = document.querySelector(".mobile-nav-toggle");
    this.createBackdrop();
    this.bindEvents();
    this.highlightActiveRoute();
  },

  createBackdrop() {
    let backdrop = document.querySelector(".sidebar-backdrop");
    if (!backdrop) {
      backdrop = document.createElement("div");
      backdrop.className = "sidebar-backdrop";
      document.body.appendChild(backdrop);
    }
    this.backdrop = backdrop;
  },

  bindEvents() {
    if (this.toggleBtn) {
      this.toggleBtn.addEventListener("click", () => this.toggleSidebar());
    }

    if (this.backdrop) {
      this.backdrop.addEventListener("click", () => this.closeSidebar());
    }

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        this.closeSidebar();
      }
    });

    // Close on link click on mobile
    const navLinks = document.querySelectorAll(".nav-link-custom");
    navLinks.forEach(link => {
      link.addEventListener("click", () => {
        if (window.innerWidth < 992) {
          this.closeSidebar();
        }
      });
    });
  },

  toggleSidebar() {
    if (this.sidebar) {
      const isOpen = this.sidebar.classList.contains("show");
      if (isOpen) {
        this.closeSidebar();
      } else {
        this.openSidebar();
      }
    }
  },

  openSidebar() {
    if (this.sidebar) {
      this.sidebar.classList.add("show");
      this.backdrop.classList.add("show");
      document.body.style.overflow = "hidden";
    }
  },

  closeSidebar() {
    if (this.sidebar) {
      this.sidebar.classList.remove("show");
      this.backdrop.classList.remove("show");
      document.body.style.overflow = "";
    }
  },

  highlightActiveRoute() {
    const currentPath = window.location.pathname.split("/").pop() || "index.html";
    const navLinks = document.querySelectorAll(".nav-link-custom");

    navLinks.forEach(link => {
      const href = link.getAttribute("href");
      if (href && href.endsWith(currentPath)) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  }
};
