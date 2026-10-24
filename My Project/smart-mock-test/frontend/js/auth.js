/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Auth Logic (Login & Register Pages)
 */

document.addEventListener("DOMContentLoaded", () => {
  AuthPage.init();
});

const AuthPage = {
  activeRole: "student",

  init() {
    this.bindRoleTabs();
    this.bindLoginForm();
    this.bindRegisterForm();
    this.bindQuickDemoFill();
    this.bindPasswordToggle();
  },

  bindRoleTabs() {
    const tabs = document.querySelectorAll(".auth-role-tab");
    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        this.activeRole = tab.getAttribute("data-role");

        const adminSecGroup = document.getElementById("adminSecurityKeyGroup");
        if (adminSecGroup) {
          adminSecGroup.style.display = this.activeRole === "admin" ? "block" : "none";
        }
      });
    });
  },

  bindLoginForm() {
    const form = document.getElementById("loginForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!Validation.validateForm(form)) return;

      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value.trim();
      const submitBtn = form.querySelector("button[type='submit']");

      try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Logging in...`;

        const res = await API.login(email, password, this.activeRole);
        App.showToast("Login successful! Redirecting...", "success");

        setTimeout(() => {
          if (res.user.role === "admin") {
            window.location.href = "admin/dashboard.html";
          } else {
            window.location.href = "student-dashboard.html";
          }
        }, 800);
      } catch (err) {
        App.showToast(err.message, "error");
        submitBtn.disabled = false;
        submitBtn.innerHTML = `Login to Account <i class="bi bi-arrow-right ms-1"></i>`;
      }
    });
  },

  bindRegisterForm() {
    const form = document.getElementById("registerForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!Validation.validateForm(form)) return;

      const name = document.getElementById("regName").value.trim();
      const email = document.getElementById("regEmail").value.trim();
      const phone = document.getElementById("regPhone").value.trim();
      const location = document.getElementById("regLocation") ? document.getElementById("regLocation").value.trim() : "India";
      const password = document.getElementById("regPassword").value.trim();
      const role = this.activeRole;

      if (role === "admin") {
        const secKey = document.getElementById("regAdminKey").value.trim();
        if (secKey !== "ADMIN2026") {
          App.showToast("Invalid Admin Security Key. Use 'ADMIN2026' for demo.", "error");
          return;
        }
      }

      const submitBtn = form.querySelector("button[type='submit']");

      try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Creating account...`;

        const res = await API.register({ name, email, phone, location, password, role });
        App.showToast("Registration successful! Redirecting...", "success");

        setTimeout(() => {
          if (res.user.role === "admin") {
            window.location.href = "admin/dashboard.html";
          } else {
            window.location.href = "student-dashboard.html";
          }
        }, 800);
      } catch (err) {
        App.showToast(err.message, "error");
        submitBtn.disabled = false;
        submitBtn.innerHTML = `Complete Registration`;
      }
    });
  },

  bindQuickDemoFill() {
    const fillStudentBtn = document.getElementById("btnFillStudentDemo");
    const fillAdminBtn = document.getElementById("btnFillAdminDemo");

    if (fillStudentBtn) {
      fillStudentBtn.addEventListener("click", () => {
        document.getElementById("loginEmail").value = "student@example.com";
        document.getElementById("loginPassword").value = "Student@123";
        const studentTab = document.querySelector(".auth-role-tab[data-role='student']");
        if (studentTab) studentTab.click();
      });
    }

    if (fillAdminBtn) {
      fillAdminBtn.addEventListener("click", () => {
        document.getElementById("loginEmail").value = "admin@example.com";
        document.getElementById("loginPassword").value = "Admin@123";
        const adminTab = document.querySelector(".auth-role-tab[data-role='admin']");
        if (adminTab) adminTab.click();
      });
    }
  },

  bindPasswordToggle() {
    const toggleBtns = document.querySelectorAll(".toggle-password-btn");
    toggleBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        const input = btn.previousElementSibling || btn.parentElement.querySelector("input");
        if (input) {
          const type = input.getAttribute("type") === "password" ? "text" : "password";
          input.setAttribute("type", type);
          const icon = btn.querySelector("i");
          if (icon) {
            icon.className = type === "password" ? "bi bi-eye" : "bi bi-eye-slash";
          }
        }
      });
    });
  }
};
