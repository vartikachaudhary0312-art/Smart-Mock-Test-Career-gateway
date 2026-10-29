/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Student Dashboard Logic
 * Resilient calculation & rendering engine with comprehensive NaN & undefined guards
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("studentDashboardView")) {
    DashboardPage.init();
  }
});

const DashboardPage = {
  async init() {
    const user = API.getCurrentUser();
    if (!user) {
      window.location.href = "login.html";
      return;
    }

    this.renderGreeting(user);
    await this.loadStats(user.id);
    await this.loadRecentTests(user.id);
    await this.loadCharts(user.id);
    await this.loadJobRecommendations();
  },

  renderGreeting(user) {
    const elem = document.getElementById("dashboardWelcomeText");
    if (elem) {
      elem.textContent = `Welcome back, ${user.name || "Student"} 👋`;
    }
  },

  async loadStats(userId) {
    let results = [];
    try {
      const rawResults = await API.getUserResults(userId);
      results = Array.isArray(rawResults) ? rawResults : [];
    } catch (e) {
      console.warn("Could not load user results for dashboard stats:", e);
    }

    let apps = [];
    try {
      apps = (await API.getUserApplications(userId)) || [];
    } catch (e) {
      console.warn("Could not load user applications for dashboard stats:", e);
    }

    const testsTaken = results.length;
    let avgScore = 0;
    let bestScore = 0;

    if (testsTaken > 0) {
      const validScores = results
        .map(r => {
          const s = Number(r.scorePct ?? r.percentage ?? r.score);
          return isNaN(s) ? null : s;
        })
        .filter(s => s !== null);

      if (validScores.length > 0) {
        const sum = validScores.reduce((acc, s) => acc + s, 0);
        avgScore = Math.round(sum / validScores.length);
        bestScore = Math.max(...validScores);
      }
    }

    // Absolute guards against NaN or infinite values
    if (isNaN(avgScore) || !isFinite(avgScore)) avgScore = 0;
    if (isNaN(bestScore) || !isFinite(bestScore)) bestScore = 0;

    const elTaken = document.getElementById("statTestsTaken");
    const elAvg = document.getElementById("statAvgScore");
    const elBest = document.getElementById("statBestScore");
    const elApps = document.getElementById("statApplications");

    if (elTaken) elTaken.textContent = testsTaken;
    if (elAvg) elAvg.textContent = `${avgScore}%`;
    if (elBest) elBest.textContent = `${bestScore}%`;
    if (elApps) elApps.textContent = apps.length;
  },

  async loadRecentTests(userId) {
    let results = [];
    try {
      const rawResults = await API.getUserResults(userId);
      results = Array.isArray(rawResults) ? rawResults : [];
    } catch (e) {
      console.warn("Could not load recent tests for dashboard:", e);
    }

    const tbody = document.getElementById("recentTestsTbody");
    const container = document.getElementById("recentTestsCardsMobile");

    if (!tbody || !container) return;

    if (results.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No mock tests attempted yet. Click "Start Mock Test" to take your first test!</td></tr>`;
      container.innerHTML = `<div class="text-center text-muted py-3">No test history available.</div>`;
      return;
    }

    let tableHtml = "";
    let mobileHtml = "";

    results.slice(0, 5).forEach(r => {
      const score = Number(r.scorePct ?? r.percentage ?? r.score ?? 0);
      const safeScore = isNaN(score) ? 0 : score;
      const subName = r.subjectName || r.subject || "General Mock Assessment";
      const diff = (r.difficulty || "medium").toLowerCase();
      const completed = r.completedAt || r.created_at || "Recent";
      const dateOnly = String(completed).split(" ")[0];
      const badgeClass = safeScore >= 75 ? "badge-green" : (safeScore >= 50 ? "badge-warning" : "badge-danger");
      const statusLabel = safeScore >= 60 ? "PASSED" : "NEEDS PRACTICE";

      tableHtml += `
        <tr>
          <td><span class="fw-semibold text-dark">${subName}</span></td>
          <td><span class="badge badge-secondary text-capitalize">${diff}</span></td>
          <td><span class="fw-bold">${safeScore}%</span></td>
          <td><span class="badge ${badgeClass}">${statusLabel}</span></td>
          <td class="small text-muted">${completed}</td>
          <td>
            <a href="result.html" class="btn btn-sm btn-outline-custom">View Analysis</a>
          </td>
        </tr>
      `;

      mobileHtml += `
        <div class="card-custom mb-3 p-3">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h6 class="mb-0 fw-bold">${subName}</h6>
            <span class="badge badge-secondary text-capitalize">${diff}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center text-muted small mb-2">
            <span>Score: <strong class="text-dark">${safeScore}%</strong></span>
            <span>Date: ${dateOnly}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center">
            <span class="badge ${badgeClass}">${statusLabel}</span>
            <a href="result.html" class="btn btn-sm btn-primary-custom py-1 px-3">Result</a>
          </div>
        </div>
      `;
    });

    tbody.innerHTML = tableHtml;
    container.innerHTML = mobileHtml;
  },

  async loadCharts(userId) {
    let results = [];
    try {
      const rawResults = await API.getUserResults(userId);
      results = Array.isArray(rawResults) ? rawResults : [];
    } catch (e) {}

    if (results.length === 0) return;

    const recent = results.slice(0, 7).reverse();
    const labels = recent.map((r, i) => `Test ${i + 1}`);
    const scores = recent.map(r => {
      const s = Number(r.scorePct ?? r.percentage ?? r.score ?? 0);
      return isNaN(s) ? 0 : s;
    });

    if (window.ChartManager) {
      ChartManager.renderScoreTrendChart("dashboardScoreTrendChart", labels, scores);
      ChartManager.renderSubjectPerformanceChart("dashboardSubjectChart", ["Java", "Python", "DSA", "DBMS", "SQL", "Web"], [80, 65, 70, 85, 90, 75]);
    }
  },

  async loadJobRecommendations() {
    let jobs = [];
    try {
      jobs = await API.getJobs();
    } catch (e) {
      console.warn("Could not load job recommendations:", e);
    }
    const container = document.getElementById("recommendedJobsContainer");
    if (!container) return;

    if (!Array.isArray(jobs) || jobs.length === 0) {
      container.innerHTML = `<div class="col-12 text-center text-muted py-3">No active job opportunities found.</div>`;
      return;
    }

    let html = "";
    jobs.filter(job => (job.status || "Active").toLowerCase() === "active").slice(0, 6).forEach(job => {
      const skillsList = Array.isArray(job.skillsRequired)
        ? job.skillsRequired
        : (Array.isArray(job.skills) ? job.skills : ["Software Engineering"]);

      const skillsBadges = skillsList.map(s => `<span class="badge badge-purple me-1 mb-1">${s}</span>`).join("");
      const jobTitle = job.title || "Software Engineering Role";
      const jobCompany = job.company || "Enterprise Partner";
      const jobLoc = job.location || "Remote, India";
      const jobSal = job.salary || "Competitive Package";

      html += `
        <div class="col-md-4 mb-3">
          <div class="job-card">
            <div>
              <div class="job-company-logo">
                <i class="bi bi-building"></i>
              </div>
              <h6 class="fw-bold mb-1">${jobTitle}</h6>
              <div class="text-muted small mb-2"><i class="bi bi-geo-alt me-1"></i>${jobCompany} • ${jobLoc}</div>
              <div class="fw-semibold text-primary mb-2">${jobSal}</div>
              <div class="job-tags mb-3">${skillsBadges}</div>
            </div>
            <a href="career.html" class="btn btn-outline-custom btn-sm w-100">View Opportunity</a>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }
};

window.DashboardPage = DashboardPage;
