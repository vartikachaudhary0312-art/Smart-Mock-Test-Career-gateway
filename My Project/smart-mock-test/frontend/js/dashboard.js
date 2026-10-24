/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Student Dashboard Logic
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
      elem.textContent = `Welcome back, ${user.name} 👋`;
    }
  },

  async loadStats(userId) {
    const results = await API.getUserResults(userId);
    const apps = await API.getUserApplications(userId);

    const testsTaken = results.length;
    const avgScore = testsTaken > 0 ? Math.round(results.reduce((acc, r) => acc + r.scorePct, 0) / testsTaken) : 0;
    const bestScore = testsTaken > 0 ? Math.max(...results.map(r => r.scorePct)) : 0;
    const totalApps = apps.length;

    document.getElementById("statTestsTaken").textContent = testsTaken;
    document.getElementById("statAvgScore").textContent = avgScore + "%";
    document.getElementById("statBestScore").textContent = bestScore + "%";
    document.getElementById("statApplications").textContent = totalApps;
  },

  async loadRecentTests(userId) {
    const results = await API.getUserResults(userId);
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
      const badgeClass = r.scorePct >= 75 ? "badge-green" : (r.scorePct >= 50 ? "badge-warning" : "badge-danger");
      
      tableHtml += `
        <tr>
          <td><span class="fw-semibold text-dark">${r.subjectName}</span></td>
          <td><span class="badge badge-secondary">${r.difficulty}</span></td>
          <td><span class="fw-bold">${r.scorePct}%</span></td>
          <td><span class="badge ${badgeClass}">${r.scorePct >= 60 ? "PASSED" : "NEEDS PRACTICE"}</span></td>
          <td class="small text-muted">${r.completedAt}</td>
          <td>
            <a href="result.html" class="btn btn-sm btn-outline-custom">View Analysis</a>
          </td>
        </tr>
      `;

      mobileHtml += `
        <div class="card-custom mb-3 p-3">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h6 class="mb-0 fw-bold">${r.subjectName}</h6>
            <span class="badge badge-secondary">${r.difficulty}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center text-muted small mb-2">
            <span>Score: <strong class="text-dark">${r.scorePct}%</strong></span>
            <span>Date: ${r.completedAt.split(" ")[0]}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center">
            <span class="badge ${badgeClass}">${r.scorePct >= 60 ? "PASSED" : "NEEDS PRACTICE"}</span>
            <a href="result.html" class="btn btn-sm btn-primary-custom py-1 px-3">Result</a>
          </div>
        </div>
      `;
    });

    tbody.innerHTML = tableHtml;
    container.innerHTML = mobileHtml;
  },

  async loadCharts(userId) {
    const results = await API.getUserResults(userId);
    if (results.length === 0) return;

    const labels = results.map((r, i) => `Test ${i + 1}`).reverse();
    const scores = results.map(r => r.scorePct).reverse();

    ChartManager.renderScoreTrendChart("dashboardScoreTrendChart", labels, scores);
    ChartManager.renderSubjectPerformanceChart("dashboardSubjectChart", ["Java", "Python", "DSA", "DBMS", "SQL", "Web"], [80, 65, 70, 85, 90, 75]);
  },

  async loadJobRecommendations() {
    const jobs = await API.getJobs();
    const container = document.getElementById("recommendedJobsContainer");
    if (!container) return;

    let html = "";
    jobs.filter(job => job.status === "Active").slice(0, 6).forEach(job => {
      const skillsBadges = job.skillsRequired.map(s => `<span class="badge badge-purple me-1 mb-1">${s}</span>`).join("");
      html += `
        <div class="col-md-4 mb-3">
          <div class="job-card">
            <div>
              <div class="job-company-logo">
                <i class="bi bi-building"></i>
              </div>
              <h6 class="fw-bold mb-1">${job.title}</h6>
              <div class="text-muted small mb-2"><i class="bi bi-geo-alt me-1"></i>${job.company} • ${job.location}</div>
              <div class="fw-semibold text-primary mb-2">${job.salary}</div>
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
