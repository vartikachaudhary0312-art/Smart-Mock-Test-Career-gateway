"""
Script to apply complete frontend updates:
- Dynamic authentication guard, login redirect, and BFCache protection in app.js
- Dynamic header and sidebar profile binding across student and admin views
- Profile page real user display and backend sync
- Mock test 50-question support and unseen-question prioritization
- Removal of demo user fallbacks (usr_student_01)
"""
import os
import re

BASE_DIR = os.path.abspath("My Project/smart-mock-test")

# 1. Update frontend/js/app.js
app_js_path = os.path.join(BASE_DIR, "frontend", "js", "app.js")
with open(app_js_path, "r", encoding="utf-8") as f:
    app_js = f.read()

app_js_content = """/**
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
    const path = window.location.pathname.replace(/\\\\/g, "/").toLowerCase();
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
    const path = window.location.pathname.replace(/\\\\/g, "/").toLowerCase();
    if (path.includes("/admin/") && user.role !== "admin") {
      window.location.replace(API.getLoginUrl());
      return false;
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
"""
with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(app_js_content)
print("Updated app.js")

# 2. Update frontend/student-dashboard.html
dash_path = os.path.join(BASE_DIR, "frontend", "student-dashboard.html")
with open(dash_path, "r", encoding="utf-8") as f:
    dash_html = f.read()

dash_html = dash_html.replace(
    '<div class="user-avatar" id="headerUserAvatar">RS</div>',
    '<div class="user-avatar" id="headerUserAvatar">--</div>'
)
dash_html = dash_html.replace(
    '<div class="fw-semibold small leading-none" id="headerUserName">Rahul Sharma</div>',
    '<div class="fw-semibold small leading-none" id="headerUserName">Student Account</div>'
)
dash_html = dash_html.replace(
    '<h2 id="dashboardWelcomeText">Welcome back, Rahul Sharma 👋</h2>',
    '<h2 id="dashboardWelcomeText">Welcome back 👋</h2>'
)
with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash_html)
print("Updated student-dashboard.html")

# 3. Update frontend/profile.html
profile_path = os.path.join(BASE_DIR, "frontend", "profile.html")
with open(profile_path, "r", encoding="utf-8") as f:
    prof_html = f.read()

prof_html = prof_html.replace(
    '<div class="user-avatar" id="headerUserAvatar">RS</div>',
    '<div class="user-avatar" id="headerUserAvatar">--</div>'
)
prof_html = prof_html.replace(
    '<div class="user-avatar mx-auto mb-3" id="profileBigAvatar" style="width: 80px; height: 80px; font-size: 2rem;">RS</div>\n                <h5 class="fw-bold text-dark mb-1">Rahul Sharma</h5>\n                <span class="badge badge-purple mb-3">MCA Candidate</span>\n                <p class="text-muted small mb-0"><i class="bi bi-geo-alt me-1"></i>Bangalore, India</p>',
    '<div class="user-avatar mx-auto mb-3" id="profileBigAvatar" style="width: 80px; height: 80px; font-size: 2rem;">--</div>\n                <h5 class="fw-bold text-dark mb-1" id="profileCardName">Student</h5>\n                <span class="badge badge-purple mb-3" id="profileCardRole">Student Candidate</span>\n                <p class="text-muted small mb-0" id="profileCardLocation"><i class="bi bi-geo-alt me-1"></i>India</p>'
)
# If newlines differ:
if 'id="profileCardName"' not in prof_html:
    prof_html = re.sub(
        r'<div class="user-avatar mx-auto mb-3" id="profileBigAvatar"[^>]*>.*?</div>\s*<h5 class="fw-bold text-dark mb-1">.*?</h5>\s*<span class="badge badge-purple mb-3">.*?</span>\s*<p class="text-muted small mb-0">.*?Bangalore, India.*?</p>',
        '<div class="user-avatar mx-auto mb-3" id="profileBigAvatar" style="width: 80px; height: 80px; font-size: 2rem;">--</div>\n                <h5 class="fw-bold text-dark mb-1" id="profileCardName">Student</h5>\n                <span class="badge badge-purple mb-3" id="profileCardRole">Student Candidate</span>\n                <p class="text-muted small mb-0" id="profileCardLocation"><i class="bi bi-geo-alt me-1"></i>India</p>',
        prof_html,
        flags=re.DOTALL
    )

prof_html = prof_html.replace('value="Rahul Sharma"', 'value="" placeholder="Enter your full name"')
prof_html = prof_html.replace('value="student@example.com"', 'value="" placeholder="name@college.edu"')
prof_html = prof_html.replace('value="+91 9876543210"', 'value="" placeholder="+91 9876543210"')
prof_html = prof_html.replace('value="Bangalore, India"', 'value="" placeholder="City, Country"')
prof_html = prof_html.replace('value="MCA 4th Sem, ABC Institute of Technology"', 'value="" placeholder="Degree, Institution"')

with open(profile_path, "w", encoding="utf-8") as f:
    f.write(prof_html)
print("Updated profile.html")

# 4. Update frontend/js/profile.js
profile_js_path = os.path.join(BASE_DIR, "frontend", "js", "profile.js")
profile_js_content = """/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Profile Management Page Logic
 * Dynamically populated from real authenticated user session and backend profile
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("profilePageView")) {
    ProfilePage.init();
  }
});

const ProfilePage = {
  async init() {
    const user = API.getCurrentUser();
    if (!user) {
      window.location.replace(API.getLoginUrl());
      return;
    }

    this.renderUserProfile(user);
    await this.fetchBackendProfile();
    this.bindSaveProfile();
  },

  renderUserProfile(user) {
    if (!user) return;

    const initials = (user.name || "Student").split(" ").map(n => n[0]).filter(Boolean).join("").substring(0, 2).toUpperCase() || "ST";

    // Bind Avatar & Card Headers
    const bigAvatar = document.getElementById("profileBigAvatar");
    const cardName = document.getElementById("profileCardName");
    const cardRole = document.getElementById("profileCardRole");
    const cardLoc = document.getElementById("profileCardLocation");

    if (bigAvatar) bigAvatar.textContent = initials;
    if (cardName) cardName.textContent = user.name || "Student";
    if (cardRole) cardRole.textContent = (user.role === "admin" ? "Administrator" : "Student Candidate");
    if (cardLoc) cardLoc.innerHTML = `<i class="bi bi-geo-alt me-1"></i>${user.location || "India"}`;

    // Bind Form Inputs
    const nameInput = document.getElementById("profileNameInput");
    const emailInput = document.getElementById("profileEmailInput");
    const phoneInput = document.getElementById("profilePhoneInput");
    const locInput = document.getElementById("profileLocationInput");
    const eduInput = document.getElementById("profileEducationInput");

    if (nameInput) nameInput.value = user.name || "";
    if (emailInput) emailInput.value = user.email || "";
    if (phoneInput) phoneInput.value = user.mobile || user.phone || "";
    if (locInput) locInput.value = user.location || "";
    if (eduInput) eduInput.value = user.education || "";
  },

  async fetchBackendProfile() {
    try {
      const token = localStorage.getItem("smt_auth_token");
      if (!token) return;

      const resp = await fetch(`${API.backendBaseUrl}/api/student/profile`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && json.data.profile) {
          const p = json.data.profile;
          const curr = API.getCurrentUser() || {};
          const merged = { ...curr, ...p };
          localStorage.setItem("smt_current_user", JSON.stringify(merged));
          this.renderUserProfile(merged);
        }
      }
    } catch (e) {
      // Offline fallback
    }
  },

  bindSaveProfile() {
    const form = document.getElementById("profileForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      const user = API.getCurrentUser();
      if (!user) {
        window.location.replace(API.getLoginUrl());
        return;
      }

      const updatedName = document.getElementById("profileNameInput").value.trim();
      const updatedPhone = document.getElementById("profilePhoneInput").value.trim();
      const updatedLoc = document.getElementById("profileLocationInput").value.trim();
      const updatedEdu = document.getElementById("profileEducationInput").value.trim();

      user.name = updatedName || user.name;
      user.mobile = updatedPhone;
      user.phone = updatedPhone;
      user.location = updatedLoc;
      user.education = updatedEdu;

      // Save locally
      localStorage.setItem("smt_current_user", JSON.stringify(user));
      const users = JSON.parse(localStorage.getItem("smt_users") || "[]");
      const idx = users.findIndex(u => String(u.id) === String(user.id) || u.email.toLowerCase() === user.email.toLowerCase());
      if (idx !== -1) {
        users[idx] = { ...users[idx], ...user };
        localStorage.setItem("smt_users", JSON.stringify(users));
      }

      // Sync with backend API
      try {
        const token = localStorage.getItem("smt_auth_token");
        if (token) {
          await fetch(`${API.backendBaseUrl}/api/student/profile`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
              name: user.name,
              mobile: user.mobile,
              location: user.location,
              education: user.education
            })
          });
        }
      } catch (err) {
        // Backend offline
      }

      this.renderUserProfile(user);
      App.initHeaderUser();
      App.showToast("Profile details updated successfully!", "success");
    });
  }
};
"""
with open(profile_js_path, "w", encoding="utf-8") as f:
    f.write(profile_js_content)
print("Updated profile.js")

# 5. Remove demo fallback in applications.js
apps_js_path = os.path.join(BASE_DIR, "frontend", "js", "applications.js")
with open(apps_js_path, "r", encoding="utf-8") as f:
    apps_js = f.read()

apps_js = apps_js.replace(
    'const user = API.getCurrentUser() || { id: "usr_student_01" };',
    'const user = API.getCurrentUser();\n    if (!user) { window.location.replace(API.getLoginUrl()); return; }'
)
with open(apps_js_path, "w", encoding="utf-8") as f:
    f.write(apps_js)
print("Updated applications.js")

# 6. Update career.js: remove demo fallbacks and handle 50 questions
career_js_path = os.path.join(BASE_DIR, "frontend", "js", "career.js")
with open(career_js_path, "r", encoding="utf-8") as f:
    career_js = f.read()

career_js = career_js.replace(
    'const user = API.getCurrentUser() || { id: "usr_student_01" };',
    'const user = API.getCurrentUser();'
)
career_js = career_js.replace(
    'if (val === "all") {',
    'if (val === "all" || val === "max") {\n          this.selectedLength = "all";\n        } else if (val === "50") {\n          this.selectedLength = 50;'
)
with open(career_js_path, "w", encoding="utf-8") as f:
    f.write(career_js)
print("Updated career.js")

# 7. Add 50 Questions option to career.html topicConfigModal
career_html_path = os.path.join(BASE_DIR, "frontend", "career.html")
with open(career_html_path, "r", encoding="utf-8") as f:
    c_html = f.read()

old_len_block = '''                <div class="config-option-card" data-len="20">
                  <div class="fw-bold">20 Questions</div>
                  <div class="small text-muted">In-depth assessment (~30 mins)</div>
                </div>'''

new_len_block = '''                <div class="config-option-card" data-len="20">
                  <div class="fw-bold">20 Questions</div>
                  <div class="small text-muted">In-depth assessment (~30 mins)</div>
                </div>
                <div class="config-option-card" data-len="50">
                  <div class="fw-bold">50 Questions</div>
                  <div class="small text-muted">Comprehensive examination (~60 mins)</div>
                </div>'''

if old_len_block in c_html:
    c_html = c_html.replace(old_len_block, new_len_block)
    with open(career_html_path, "w", encoding="utf-8") as f:
        f.write(c_html)
    print("Updated career.html with 50 Questions card")

# 8. Update mock-test.js:
# - startActualTest loads questions from backend (with length: reqCount) and falls back to prioritized local pool
# - submitFinalTest resolves correctIndex and explanation from API._getQuestionsStore()
# - removes fallback usr_student_01
mock_test_js_path = os.path.join(BASE_DIR, "frontend", "js", "mock-test.js")
with open(mock_test_js_path, "r", encoding="utf-8") as f:
    mt_js = f.read()

# Replace usr_student_01
mt_js = mt_js.replace(
    'const user = API.getCurrentUser() || { id: "usr_student_01" };',
    'const user = API.getCurrentUser();\n    if (!user) {\n      window.location.replace(API.getLoginUrl());\n      return;\n    }'
)

# In submitFinalTest: resolve review from store
old_review_block = '''    this.questions.forEach(q => {
      const userOpt = this.userAnswers[q.id];
      if (userOpt === undefined) {
        skipped++;
        detailedReview.push({ ...q, userOpt: null, status: "skipped" });
      } else if (userOpt === q.correctIndex) {
        correct++;
        detailedReview.push({ ...q, userOpt, status: "correct" });
      } else {
        incorrect++;
        detailedReview.push({ ...q, userOpt, status: "incorrect" });
      }
    });'''

new_review_block = '''    const storeQuestions = (API._getQuestionsStore && API._getQuestionsStore()) || [];
    const storeMap = new Map(storeQuestions.map(item => [String(item.id), item]));

    this.questions.forEach(q => {
      const fullQ = storeMap.get(String(q.id)) || q;
      let targetCorrectIdx = fullQ.correctIndex;
      if (targetCorrectIdx === undefined && fullQ.correct_option) {
        targetCorrectIdx = { "A": 0, "B": 1, "C": 2, "D": 3 }[String(fullQ.correct_option).toUpperCase()];
      }
      if (targetCorrectIdx === undefined) targetCorrectIdx = 0;

      const userOpt = this.userAnswers[q.id];
      if (userOpt === undefined) {
        skipped++;
        detailedReview.push({ ...fullQ, userOpt: null, status: "skipped", correctIndex: targetCorrectIdx });
      } else if (userOpt === targetCorrectIdx) {
        correct++;
        detailedReview.push({ ...fullQ, userOpt, status: "correct", correctIndex: targetCorrectIdx });
      } else {
        incorrect++;
        detailedReview.push({ ...fullQ, userOpt, status: "incorrect", correctIndex: targetCorrectIdx });
      }
    });'''

if old_review_block in mt_js:
    mt_js = mt_js.replace(old_review_block, new_review_block)
    print("Replaced review block in mock-test.js")

# In startActualTest: support length: reqCount and backend questions
old_start_actual = '''    const reqCount = this.selectedLength === "max" ? 9999 : (parseInt(this.selectedLength, 10) || 10);
    this.testSubjectLabel = this.selectedSubject ? this.selectedSubject.name : "Mock Test";
    this.testDifficultyLabel = this.selectedDifficulty || "Medium";

    // 1. Fetch questions for the selected subject and difficulty
    let questions = await API.getQuestions(this.selectedSubject?.id, this.selectedDifficulty);

    // 2. Fallback to any difficulty of this subject if specific level is empty
    if (questions.length === 0 && this.selectedDifficulty && this.selectedDifficulty.toLowerCase() !== "mixed") {
      questions = await API.getQuestions(this.selectedSubject?.id);
      this.testDifficultyLabel = "All Levels";
    }

    // 3. If still 0 questions, cleanly inform candidate
    if (questions.length === 0) {
      this.goToStep(1);
      App.showToast(`Questions coming soon for ${this.testSubjectLabel}. Please select another subject in the meantime.`, "info");
      return;
    }

    // 4. Limit to requested length
    this.questions = this.shuffleQuestions(questions).slice(0, reqCount);

    // Dynamic duration: 1.5 minutes per question, minimum 10 minutes
    const dynamicMins = Math.max(10, Math.round(this.questions.length * 1.5));
    this.timerSeconds = dynamicMins * 60;
    this.initialTimerSeconds = this.timerSeconds;

    // Backend Session & Attempt Initialization
    let attemptId = `att_${Date.now()}_${this.selectedSubject?.id || 1}`;
    try {
      const token = localStorage.getItem("smt_auth_token") || "";
      const testIdToStart = this.selectedSubject?.id || 1;
      const resp = await fetch(`${API.backendBaseUrl}/api/tests/${testIdToStart}/start`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          difficulty: this.selectedDifficulty,
          length: this.questions.length
        })
      });
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && json.data.attempt_id) {
          attemptId = json.data.attempt_id;
        }
      }
    } catch (err) {
      console.warn("[MockTestEngine] Backend start fallback to client session ID:", err);
    }
    this.currentAttemptId = attemptId;'''

new_start_actual = '''    const reqCount = this.selectedLength === "max" ? 9999 : (parseInt(this.selectedLength, 10) || 50);
    this.testSubjectLabel = this.selectedSubject ? this.selectedSubject.name : "Mock Test";
    this.testDifficultyLabel = this.selectedDifficulty || "Medium";

    // 1. Attempt to start proctored session directly via Backend API with rotation
    let backendQuestions = null;
    let attemptId = `att_${Date.now()}_${this.selectedSubject?.id || 1}`;
    try {
      const token = localStorage.getItem("smt_auth_token") || "";
      const testIdToStart = this.selectedSubject?.id || 1;
      const resp = await fetch(`${API.backendBaseUrl}/api/tests/${testIdToStart}/start`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          difficulty: this.selectedDifficulty,
          length: reqCount
        })
      });
      if (resp.ok) {
        const json = await resp.json();
        if (json.data) {
          if (json.data.attempt_id) attemptId = json.data.attempt_id;
          if (Array.isArray(json.data.questions) && json.data.questions.length > 0) {
            backendQuestions = json.data.questions;
          }
        }
      }
    } catch (err) {
      console.warn("[MockTestEngine] Backend start fallback to client session ID:", err);
    }
    this.currentAttemptId = attemptId;

    if (backendQuestions && backendQuestions.length > 0) {
      this.questions = backendQuestions;
    } else {
      // Offline fallback: fetch from client questions bank
      let questions = await API.getQuestions(this.selectedSubject?.id, this.selectedDifficulty);

      if (questions.length === 0 && this.selectedDifficulty && this.selectedDifficulty.toLowerCase() !== "mixed") {
        questions = await API.getQuestions(this.selectedSubject?.id);
        this.testDifficultyLabel = "All Levels";
      }

      if (questions.length === 0) {
        this.goToStep(1);
        App.showToast(`Questions coming soon for ${this.testSubjectLabel}. Please select another subject in the meantime.`, "info");
        return;
      }

      // Prioritize unseen questions locally
      const currentUser = API.getCurrentUser();
      const pastResults = currentUser ? await API.getUserResults(currentUser.id) : [];
      const seenQIds = new Set();
      pastResults.forEach(r => {
        if (Array.isArray(r.questionIds)) {
          r.questionIds.forEach(id => seenQIds.add(String(id)));
        }
      });

      const unseen = questions.filter(q => !seenQIds.has(String(q.id)));
      const seen = questions.filter(q => seenQIds.has(String(q.id)));
      const pool = [...this.shuffleQuestions(unseen), ...this.shuffleQuestions(seen)];
      this.questions = pool.slice(0, reqCount);
    }

    // Dynamic duration: 1.5 minutes per question, minimum 10 minutes
    const dynamicMins = Math.max(10, Math.round(this.questions.length * 1.5));
    this.timerSeconds = dynamicMins * 60;
    this.initialTimerSeconds = this.timerSeconds;'''

if old_start_actual in mt_js:
    mt_js = mt_js.replace(old_start_actual, new_start_actual)
    print("Replaced startActualTest in mock-test.js")

with open(mock_test_js_path, "w", encoding="utf-8") as f:
    f.write(mt_js)
print("Updated mock-test.js")

print("All frontend updates applied successfully!")

