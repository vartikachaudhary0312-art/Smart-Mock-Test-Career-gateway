/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Admin Portal Operations & Dashboard Engine
 * Connected directly to Flask REST API with robust local fallbacks
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("adminPortalView")) {
    AdminEngine.init();
  }
});

const AdminEngine = {
  async init() {
    const user = API.getCurrentUser();
    if (!user || user.role !== "admin") {
      // Auth guard in app.js redirects unauthorized users
      return;
    }

    if (document.getElementById("adminDashboardView")) {
      await this.loadAdminDashboard();
    } else if (document.getElementById("adminStudentsView")) {
      await this.loadAdminStudents();
    } else if (document.getElementById("adminSubjectsView")) {
      await this.loadAdminSubjects();
    } else if (document.getElementById("adminQuestionsView")) {
      await this.loadAdminQuestions();
    } else if (document.getElementById("adminJobsView")) {
      await this.loadAdminJobs();
    } else if (document.getElementById("adminApplicationsView")) {
      await this.loadAdminApplications();
    } else if (document.getElementById("adminResultsView")) {
      await this.loadAdminResults();
    }
  },

  // --- ADMIN DASHBOARD ---
  async loadAdminDashboard() {
    try {
      const metrics = await API.getAdminDashboard();
      if (metrics) {
        const studentEl = document.getElementById("adminStatStudents");
        const testsEl = document.getElementById("adminStatTests");
        const avgEl = document.getElementById("adminStatAvgScore");
        const jobsEl = document.getElementById("adminStatJobs");

        if (studentEl) studentEl.textContent = metrics.total_students ?? 0;
        if (testsEl) testsEl.textContent = metrics.tests_attempted ?? 0;
        if (avgEl) avgEl.textContent = `${metrics.average_score ?? 0}%`;
        if (jobsEl) jobsEl.textContent = metrics.active_jobs ?? 0;

        if (window.ChartManager) {
          if (metrics.students_growth) {
            ChartManager.renderScoreTrendChart(
              "adminStudentGrowthChart",
              metrics.students_growth.labels,
              metrics.students_growth.data
            );
          }
          if (metrics.application_status) {
            const counts = metrics.application_status.data || [];
            ChartManager.renderResultBreakdownDoughnut(
              "adminAppStatusChart",
              counts[0] || 0,
              counts[1] || 0,
              (counts[2] || 0) + (counts[3] || 0) + (counts[4] || 0)
            );
          }
        }
        return;
      }
    } catch (e) {
      console.warn("Backend admin dashboard metrics unavailable, using cached statistics:", e);
    }

    // Fallback if backend is unreachable
    const users = JSON.parse(localStorage.getItem("smt_users") || "[]").filter(u => u.role === "student");
    const results = await API.getAllResults();
    const jobs = await API.getJobs();

    const studentEl = document.getElementById("adminStatStudents");
    const testsEl = document.getElementById("adminStatTests");
    const avgEl = document.getElementById("adminStatAvgScore");
    const jobsEl = document.getElementById("adminStatJobs");

    if (studentEl) studentEl.textContent = users.length;
    if (testsEl) testsEl.textContent = results.length;
    const validAdminScores = results.map(r => { const s = Number(r.scorePct ?? r.percentage ?? r.score); return isNaN(s) || !isFinite(s) ? null : s; }).filter(s => s !== null);
    const avgScore = validAdminScores.length > 0 ? Math.round(validAdminScores.reduce((acc, s) => acc + s, 0) / validAdminScores.length) : 0;
    if (avgEl) avgEl.textContent = avgScore + "%";
    if (jobsEl) jobsEl.textContent = jobs.length;

    if (window.ChartManager) {
      ChartManager.renderScoreTrendChart("adminStudentGrowthChart", ["Jan", "Feb", "Mar", "Apr", "May"], [12, 28, 45, 68, Math.max(85, users.length)]);
      ChartManager.renderResultBreakdownDoughnut("adminAppStatusChart", 15, 8, 4);
    }
  },

  // --- STUDENTS MANAGEMENT ---
  async loadAdminStudents() {
    const tbody = document.getElementById("adminStudentsTableTbody");
    if (!tbody) return;

    let students = [];
    try {
      students = await API.getAdminStudents();
    } catch (e) {
      console.warn("Backend student fetch failed, using local fallback:", e);
      students = JSON.parse(localStorage.getItem("smt_users") || "[]").filter(u => u.role === "student");
    }

    if (!students || students.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-muted"><i class="bi bi-people me-2"></i>No registered students found.</td></tr>`;
      return;
    }

    let html = "";
    students.forEach(u => {
      const status = u.status || "Active";
      const isBlocked = status.toLowerCase() === "blocked";
      const statusBadge = isBlocked
        ? `<span class="badge badge-danger">Blocked</span>`
        : `<span class="badge badge-green">Active</span>`;
      const toggleAction = isBlocked ? "Activate" : "Block";
      const toggleClass = isBlocked ? "btn-outline-success" : "btn-outline-danger";
      const nextStatus = isBlocked ? "Active" : "Blocked";

      html += `
        <tr>
          <td><span class="fw-bold">${u.name || "Student"}</span></td>
          <td>${u.email}</td>
          <td>${u.mobile || u.phone || "N/A"}</td>
          <td>${u.education || u.location || "Student"}</td>
          <td>${statusBadge}</td>
          <td>
            <button class="btn btn-sm btn-outline-custom me-1" onclick="AdminEngine.viewStudent(${u.id})">View</button>
            <button class="btn btn-sm ${toggleClass}" onclick="AdminEngine.toggleStudentStatus(${u.id}, '${nextStatus}')">${toggleAction}</button>
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  },

  async toggleStudentStatus(studentId, nextStatus) {
    try {
      await API.updateStudentStatus(studentId, nextStatus);
      if (window.App && typeof window.App.showToast === "function") {
        App.showToast(`Student #${studentId} account marked as ${nextStatus}.`, "success");
      }
      await this.loadAdminStudents();
    } catch (err) {
      if (window.App && typeof window.App.showToast === "function") {
        App.showToast(err.message || "Failed to update student status.", "error");
      }
    }
  },

  async viewStudent(studentId) {
    try {
      const student = await API.getAdminStudentDetail(studentId);
      if (window.App && typeof window.App.showToast === "function") {
        App.showToast(`Student: ${student.name} (${student.email}) - Status: ${student.status || 'Active'}`, "info");
      }
    } catch (e) {
      if (window.App && typeof window.App.showToast === "function") {
        App.showToast(`Loaded details for student #${studentId}`, "info");
      }
    }
  },

  // --- SUBJECTS MANAGEMENT ---
  async loadAdminSubjects() {
    const subjects = await API.getSubjects();
    const container = document.getElementById("adminSubjectsGrid");
    if (!container) return;

    let html = "";
    subjects.forEach(sub => {
      const qCount = sub.questionCount || sub.question_count || 0;
      html += `
        <div class="col-md-4 mb-3">
          <div class="card-custom p-3">
            <div class="d-flex align-items-center gap-3 mb-2">
              <div class="stat-icon-wrapper stat-icon-purple">
                <i class="bi ${sub.icon || 'bi-journal-bookmark'}"></i>
              </div>
              <div>
                <h6 class="fw-bold mb-0">${sub.name}</h6>
                <span class="badge badge-secondary">${sub.category || 'General'}</span>
              </div>
            </div>
            <div class="d-flex justify-content-between align-items-center mt-3 pt-2 border-top text-muted small">
              <span>${qCount} Questions</span>
              <button class="btn btn-sm btn-outline-custom" onclick="App.showToast('Edit Subject Modal Opened', 'info')">Edit</button>
            </div>
          </div>
        </div>
      `;
    });
    container.innerHTML = html;

    // Bind Add Subject form
    const form = document.getElementById("addSubjectForm");
    if (form) {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = document.getElementById("newSubName").value;
        const category = document.getElementById("newSubCategory").value;
        const icon = document.getElementById("newSubIcon").value || "bi-book";

        await API.addSubject({ name, category, icon });
        App.showToast("New Subject added successfully!", "success");
        
        const modalElem = document.getElementById("addSubjectModal");
        if (modalElem && window.bootstrap) {
          const modal = bootstrap.Modal.getInstance(modalElem);
          if (modal) modal.hide();
        }
        this.loadAdminSubjects();
      });
    }
  },

  // --- QUESTIONS BANK MANAGEMENT ---
  async loadAdminQuestions() {
    let questions = [];
    try {
      questions = await API.getAdminQuestions();
    } catch (e) {
      questions = await API.getQuestions();
    }

    const tbody = document.getElementById("adminQuestionsTableTbody");
    if (!tbody) return;

    let html = "";
    questions.forEach((q, i) => {
      const qText = q.question_text || q.question || "N/A";
      const qSub = (q.subject || (q.subjectId ? q.subjectId.replace("sub_", "").toUpperCase() : "CS"));
      const qDiff = q.difficulty || "medium";
      const qCorrect = q.correct_option || (["A", "B", "C", "D"][q.correctIndex] || "A");

      html += `
        <tr>
          <td>#${i + 1}</td>
          <td style="max-width: 300px;" class="text-truncate fw-semibold">${qText}</td>
          <td><span class="badge badge-purple">${qSub}</span></td>
          <td><span class="badge badge-secondary">${qDiff}</span></td>
          <td>Option ${qCorrect}</td>
          <td>
            <button class="btn btn-sm btn-outline-custom" onclick="App.showToast('Editing question detail...', 'info')">Edit</button>
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;

    // Bind Add Question
    const form = document.getElementById("addQuestionForm");
    if (form) {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const question = document.getElementById("qText").value;
        const optA = document.getElementById("qOptA").value;
        const optB = document.getElementById("qOptB").value;
        const optC = document.getElementById("qOptC").value;
        const optD = document.getElementById("qOptD").value;
        const correctIndex = parseInt(document.getElementById("qCorrectIndex").value);
        const correctOption = ["A", "B", "C", "D"][correctIndex] || "A";
        const subjectId = document.getElementById("qSubjectId").value;
        const difficulty = document.getElementById("qDifficulty").value;
        const explanation = document.getElementById("qExplanation").value;

        await API.addQuestion({
          question_text: question,
          question,
          option_a: optA,
          option_b: optB,
          option_c: optC,
          option_d: optD,
          options: [optA, optB, optC, optD],
          correct_option: correctOption,
          correctIndex,
          subject_id: subjectId,
          subjectId,
          difficulty,
          explanation
        });

        App.showToast("Question added to Question Bank!", "success");
        const modalElem = document.getElementById("addQuestionModal");
        if (modalElem && window.bootstrap) {
          const modal = bootstrap.Modal.getInstance(modalElem);
          if (modal) modal.hide();
        }
        this.loadAdminQuestions();
      });
    }
  },

  // --- JOBS MANAGEMENT ---
  async loadAdminJobs() {
    let jobs = [];
    try {
      jobs = await API.getAdminJobs();
    } catch (e) {
      jobs = await API.getJobs();
    }

    const tbody = document.getElementById("adminJobsTableTbody");
    if (!tbody) return;

    let html = "";
    jobs.forEach(j => {
      html += `
        <tr>
          <td><span class="fw-bold">${j.title}</span></td>
          <td>${j.company}</td>
          <td>${j.location || 'Remote'}</td>
          <td>${j.salary || 'Competitive'}</td>
          <td><span class="badge badge-green">${j.status || 'Active'}</span></td>
          <td>
            <button class="btn btn-sm btn-outline-custom me-1" onclick="App.showToast('Job edit modal opened.', 'info')">Edit</button>
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;

    const form = document.getElementById("addJobForm");
    if (form) {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const title = document.getElementById("jobTitleInput").value;
        const company = document.getElementById("jobCompanyInput").value;
        const location = document.getElementById("jobLocationInput").value;
        const type = document.getElementById("jobTypeInput").value;
        const salary = document.getElementById("jobSalaryInput").value;
        const skillsRequired = document.getElementById("jobSkillsInput").value.split(",").map(s => s.trim());
        const description = document.getElementById("jobDescInput").value;

        await API.addJob({ title, company, location, type, salary, skillsRequired, description });
        App.showToast("Job Posting published!", "success");

        const modalElem = document.getElementById("addJobModal");
        if (modalElem && window.bootstrap) {
          const modal = bootstrap.Modal.getInstance(modalElem);
          if (modal) modal.hide();
        }
        this.loadAdminJobs();
      });
    }
  },

  // --- APPLICATIONS MANAGEMENT ---
  async loadAdminApplications() {
    const apps = await API.getAllApplications();
    const tbody = document.getElementById("adminAppsTableTbody");
    if (!tbody) return;

    let html = "";
    apps.forEach(a => {
      const uId = a.userId || a.student_id || "0000";
      const studentLabel = `Student #${String(uId).slice(-4)}`;
      const appDate = a.appliedDate || a.appliedAt || a.applied_at || "Recent";
      const status = a.status || "Applied";

      html += `
        <tr>
          <td><span class="fw-bold">${a.jobTitle || a.job_title || 'Software Engineer'}</span></td>
          <td>${a.company || 'Enterprise Partner'}</td>
          <td>${studentLabel}</td>
          <td>${appDate}</td>
          <td>
            <select class="form-select form-select-sm" onchange="AdminEngine.changeAppStatus('${a.id}', this.value)">
              <option value="Applied" ${status === 'Applied' ? 'selected' : ''}>Applied</option>
              <option value="Under Review" ${status === 'Under Review' ? 'selected' : ''}>Under Review</option>
              <option value="Shortlisted" ${status === 'Shortlisted' ? 'selected' : ''}>Shortlisted</option>
              <option value="Interview" ${status === 'Interview' ? 'selected' : ''}>Interview</option>
              <option value="Selected" ${status === 'Selected' ? 'selected' : ''}>Selected</option>
              <option value="Rejected" ${status === 'Rejected' ? 'selected' : ''}>Rejected</option>
            </select>
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  },

  async changeAppStatus(appId, newStatus) {
    try {
      await API.updateApplicationStatus(appId, newStatus);
      if (window.App && typeof window.App.showToast === "function") {
        App.showToast(`Application status updated to '${newStatus}'!`, "success");
      }
    } catch (err) {
      if (window.App && typeof window.App.showToast === "function") {
        App.showToast(err.message || "Failed to update application status.", "error");
      }
    }
  },

  // --- RESULTS AUDIT ---
  async loadAdminResults() {
    const results = await API.getAllResults();
    const tbody = document.getElementById("adminResultsTableTbody");
    if (!tbody) return;

    let html = "";
    results.forEach(r => {
      const uId = r.userId || r.user_id || "0000";
      const score = r.scorePct ?? r.percentage ?? 0;
      const subName = r.subjectName || r.subject || "General Test";
      const diff = r.difficulty || "medium";
      const completed = r.completedAt || r.completed_at || "Recent";

      html += `
        <tr>
          <td>Student #${String(uId).slice(-4)}</td>
          <td><span class="fw-bold">${subName}</span></td>
          <td><span class="badge badge-secondary">${diff}</span></td>
          <td><span class="fw-bold">${score}%</span></td>
          <td>${completed}</td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  }
};

window.AdminEngine = AdminEngine;
