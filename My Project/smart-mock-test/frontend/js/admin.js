/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Admin Portal Operations & Dashboard Engine
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
      // Allow demo viewing if logged as student with toast warning or auto redirect
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
    const users = JSON.parse(localStorage.getItem("smt_users") || "[]").filter(u => u.role === "student");
    const results = await API.getAllResults();
    const jobs = await API.getJobs();
    const apps = await API.getAllApplications();

    document.getElementById("adminStatStudents").textContent = users.length;
    document.getElementById("adminStatTests").textContent = results.length;
    const avgScore = results.length > 0 ? Math.round(results.reduce((acc, r) => acc + r.scorePct, 0) / results.length) : 0;
    document.getElementById("adminStatAvgScore").textContent = avgScore + "%";
    document.getElementById("adminStatJobs").textContent = jobs.length;

    // Charts
    ChartManager.renderScoreTrendChart("adminStudentGrowthChart", ["Jan", "Feb", "Mar", "Apr", "May"], [12, 28, 45, 68, 85]);
    ChartManager.renderResultBreakdownDoughnut("adminAppStatusChart", 15, 8, 4);
  },

  // --- STUDENTS MANAGEMENT ---
  async loadAdminStudents() {
    const users = JSON.parse(localStorage.getItem("smt_users") || "[]").filter(u => u.role === "student");
    const tbody = document.getElementById("adminStudentsTableTbody");
    if (!tbody) return;

    let html = "";
    users.forEach(u => {
      html += `
        <tr>
          <td><span class="fw-bold">${u.name}</span></td>
          <td>${u.email}</td>
          <td>${u.phone || "N/A"}</td>
          <td>${u.education || "MCA Student"}</td>
          <td><span class="badge badge-green">Active</span></td>
          <td>
            <button class="btn btn-sm btn-outline-custom me-1" onclick="App.showToast('Student profile details loaded.', 'info')">View</button>
            <button class="btn btn-sm btn-outline-danger" onclick="App.showToast('Student account status toggled.', 'warning')">Block</button>
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  },

  // --- SUBJECTS MANAGEMENT ---
  async loadAdminSubjects() {
    const subjects = await API.getSubjects();
    const container = document.getElementById("adminSubjectsGrid");
    if (!container) return;

    let html = "";
    subjects.forEach(sub => {
      html += `
        <div class="col-md-4 mb-3">
          <div class="card-custom p-3">
            <div class="d-flex align-items-center gap-3 mb-2">
              <div class="stat-icon-wrapper stat-icon-purple">
                <i class="bi ${sub.icon}"></i>
              </div>
              <div>
                <h6 class="fw-bold mb-0">${sub.name}</h6>
                <span class="badge badge-secondary">${sub.category}</span>
              </div>
            </div>
            <div class="d-flex justify-content-between align-items-center mt-3 pt-2 border-top text-muted small">
              <span>${sub.questionCount} Questions</span>
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
        const modal = bootstrap.Modal.getInstance(modalElem);
        if (modal) modal.hide();
        this.loadAdminSubjects();
      });
    }
  },

  // --- QUESTIONS BANK MANAGEMENT ---
  async loadAdminQuestions() {
    const questions = await API.getQuestions();
    const tbody = document.getElementById("adminQuestionsTableTbody");
    if (!tbody) return;

    let html = "";
    questions.forEach((q, i) => {
      html += `
        <tr>
          <td>#${i + 1}</td>
          <td style="max-width: 300px;" class="text-truncate fw-semibold">${q.question}</td>
          <td><span class="badge badge-purple">${q.subjectId.replace("sub_", "").toUpperCase()}</span></td>
          <td><span class="badge badge-secondary">${q.difficulty}</span></td>
          <td>Option ${["A", "B", "C", "D"][q.correctIndex]}</td>
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
        const subjectId = document.getElementById("qSubjectId").value;
        const difficulty = document.getElementById("qDifficulty").value;
        const explanation = document.getElementById("qExplanation").value;

        await API.addQuestion({
          question,
          options: [optA, optB, optC, optD],
          correctIndex,
          subjectId,
          difficulty,
          explanation
        });

        App.showToast("Question added to Question Bank!", "success");
        const modalElem = document.getElementById("addQuestionModal");
        const modal = bootstrap.Modal.getInstance(modalElem);
        if (modal) modal.hide();
        this.loadAdminQuestions();
      });
    }
  },

  // --- JOBS MANAGEMENT ---
  async loadAdminJobs() {
    const jobs = await API.getJobs();
    const tbody = document.getElementById("adminJobsTableTbody");
    if (!tbody) return;

    let html = "";
    jobs.forEach(j => {
      html += `
        <tr>
          <td><span class="fw-bold">${j.title}</span></td>
          <td>${j.company}</td>
          <td>${j.location}</td>
          <td>${j.salary}</td>
          <td><span class="badge badge-green">${j.status}</span></td>
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
        const modal = bootstrap.Modal.getInstance(modalElem);
        if (modal) modal.hide();
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
      html += `
        <tr>
          <td><span class="fw-bold">${a.jobTitle}</span></td>
          <td>${a.company}</td>
          <td>Student #${a.userId.slice(-4)}</td>
          <td>${a.appliedDate}</td>
          <td>
            <select class="form-select form-select-sm" onchange="AdminEngine.changeAppStatus('${a.id}', this.value)">
              <option value="Applied" ${a.status === 'Applied' ? 'selected' : ''}>Applied</option>
              <option value="Under Review" ${a.status === 'Under Review' ? 'selected' : ''}>Under Review</option>
              <option value="Shortlisted" ${a.status === 'Shortlisted' ? 'selected' : ''}>Shortlisted</option>
              <option value="Interview" ${a.status === 'Interview' ? 'selected' : ''}>Interview</option>
              <option value="Selected" ${a.status === 'Selected' ? 'selected' : ''}>Selected</option>
              <option value="Rejected" ${a.status === 'Rejected' ? 'selected' : ''}>Rejected</option>
            </select>
          </td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  },

  async changeAppStatus(appId, newStatus) {
    await API.updateApplicationStatus(appId, newStatus);
    App.showToast(`Application status updated to '${newStatus}'!`, "success");
  },

  // --- RESULTS AUDIT ---
  async loadAdminResults() {
    const results = await API.getAllResults();
    const tbody = document.getElementById("adminResultsTableTbody");
    if (!tbody) return;

    let html = "";
    results.forEach(r => {
      html += `
        <tr>
          <td>Student #${r.userId.slice(-4)}</td>
          <td><span class="fw-bold">${r.subjectName}</span></td>
          <td><span class="badge badge-secondary">${r.difficulty}</span></td>
          <td><span class="fw-bold">${r.scorePct}%</span></td>
          <td>${r.completedAt}</td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  }
};

window.AdminEngine = AdminEngine;
