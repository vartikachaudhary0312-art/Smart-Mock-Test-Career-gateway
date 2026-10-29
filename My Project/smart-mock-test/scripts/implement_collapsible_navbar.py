"""
Script to implement Collapsible Student Portal Navbar across:
- frontend/css/global.css
- frontend/css/responsive.css
- frontend/js/navigation.js
- 8 Student Portal HTML files
"""
import os
import re

BASE_DIR = os.path.abspath("My Project/smart-mock-test")

# 1. Update frontend/css/global.css
global_css_path = os.path.join(BASE_DIR, "frontend", "css", "global.css")
with open(global_css_path, "r", encoding="utf-8") as f:
    global_css = f.read()

# Append or inject the student portal collapsible sidebar CSS rules
student_sidebar_css = """
/* ========================================================
   STUDENT PORTAL COLLAPSIBLE SIDEBAR NAVIGATION (ALL SCREENS)
   ======================================================== */

/* Student Portal: Sidebar hidden by default offcanvas */
body:not(#adminPortalView) .app-sidebar {
  width: var(--sidebar-width);
  background-color: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1045;
  transform: translateX(-100%);
  box-shadow: none;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
}

/* Student Portal: Sidebar opened via hamburger */
body:not(#adminPortalView) .app-sidebar.show {
  transform: translateX(0);
  box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.28), 0 0 24px rgba(124, 58, 237, 0.16);
}

/* Student Portal: Main content takes full screen width */
body:not(#adminPortalView) .app-main {
  margin-left: 0;
  width: 100%;
  max-width: 100%;
  transition: none;
}

/* Student Portal: Modern compact hamburger button at top-left */
body:not(#adminPortalView) .mobile-nav-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  padding: 0;
  border: 1px solid var(--border);
  background-color: var(--surface-subtle);
  color: var(--text);
  border-radius: var(--radius-md);
  font-size: 1.35rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

body:not(#adminPortalView) .mobile-nav-toggle:hover {
  background-color: var(--border-subtle);
  color: var(--primary);
  border-color: var(--primary-light);
}

body:not(#adminPortalView) .mobile-nav-toggle:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* Sidebar Header Close Button */
.sidebar-close-btn {
  margin-left: auto;
  background: transparent;
  border: none;
  color: var(--muted);
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.05rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.sidebar-close-btn:hover {
  background-color: var(--surface-subtle);
  color: var(--danger);
}

.sidebar-close-btn:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* Universal Backdrop Overlay */
.sidebar-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(2px);
  z-index: 1040;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--transition-normal);
}

.sidebar-backdrop.show {
  opacity: 1;
  pointer-events: auto;
}
"""

if "/* STUDENT PORTAL COLLAPSIBLE SIDEBAR NAVIGATION" not in global_css:
    global_css += "\n" + student_sidebar_css
    with open(global_css_path, "w", encoding="utf-8") as f:
        f.write(global_css)
    print("Updated global.css with student collapsible navbar rules")

# 2. Update frontend/js/navigation.js
nav_js_path = os.path.join(BASE_DIR, "frontend", "js", "navigation.js")
nav_js_content = """/**
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
    const rawPath = window.location.pathname.replace(/\\\\/g, "/");
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
"""
with open(nav_js_path, "w", encoding="utf-8") as f:
    f.write(nav_js_content)
print("Updated navigation.js")

# 3. Update the 8 Student Portal HTML files
student_pages = [
    "student-dashboard.html",
    "mock-test.html",
    "result.html",
    "resume.html",
    "career.html",
    "applications.html",
    "profile.html",
    "settings.html"
]

old_header_pat = re.compile(
    r'<div class="sidebar-header">\s*<div class="brand-logo"><i class="bi bi-mortarboard-fill"></i></div>\s*<div class="brand-text">SMART MOCK TEST<span>CAREER GATEWAY</span></div>\s*</div>'
)

new_header_snippet = '''<div class="sidebar-header">
        <div class="d-flex align-items-center gap-2">
          <div class="brand-logo"><i class="bi bi-mortarboard-fill"></i></div>
          <div class="brand-text">SMART MOCK TEST<span>CAREER GATEWAY</span></div>
        </div>
        <button class="sidebar-close-btn" type="button" aria-label="Close Navigation Menu"><i class="bi bi-x-lg"></i></button>
      </div>'''

toggle_pat = re.compile(
    r'<button class="mobile-nav-toggle" type="button"><i class="bi bi-list"></i></button>'
)

new_toggle_snippet = '''<button class="mobile-nav-toggle" id="btnSidebarToggle" type="button" aria-label="Toggle Navigation Menu" aria-expanded="false" title="Menu"><i class="bi bi-list"></i></button>'''

for p in student_pages:
    fpath = os.path.join(BASE_DIR, "frontend", p)
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # Add close button inside sidebar header if not present
    if "sidebar-close-btn" not in html:
        html, count = old_header_pat.subn(new_header_snippet, html)
        if count == 0:
            # Fallback simple string replace
            simple_old = '<div class="sidebar-header">\n        <div class="brand-logo"><i class="bi bi-mortarboard-fill"></i></div>\n        <div class="brand-text">SMART MOCK TEST<span>CAREER GATEWAY</span></div>\n      </div>'
            html = html.replace(simple_old, new_header_snippet)

    # Enhance hamburger button
    html = toggle_pat.sub(new_toggle_snippet, html)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated {p}")

print("All Collapsible Navbar updates applied successfully!")

