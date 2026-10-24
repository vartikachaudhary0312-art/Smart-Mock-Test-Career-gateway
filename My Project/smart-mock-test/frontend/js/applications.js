/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Student Application Tracker Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("applicationsTrackerView")) {
    ApplicationsPage.init();
  }
});

const ApplicationsPage = {
  async init() {
    const user = API.getCurrentUser() || { id: "usr_student_01" };
    await this.loadApplications(user.id);
  },

  async loadApplications(userId) {
    const apps = await API.getUserApplications(userId);
    const container = document.getElementById("applicationsListContainer");
    const tbody = document.getElementById("applicationsTableTbody");

    if (!tbody || !container) return;

    if (apps.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-4">You have not submitted any job applications yet. Visit Career Gateway to apply!</td></tr>`;
      container.innerHTML = `
        <div class="empty-state card-custom">
          <i class="bi bi-file-earmark-check empty-state-icon"></i>
          <div class="empty-state-title">No Active Applications</div>
          <div class="empty-state-desc">Explore tailored job recommendations and submit applications directly from the Career Gateway.</div>
          <a href="career.html" class="btn btn-primary-custom">Explore Career Gateway</a>
        </div>
      `;
      return;
    }

    let tableHtml = "";
    let mobileHtml = "";

    apps.forEach(app => {
      let badgeClass = "badge-purple";
      if (app.status === "Shortlisted") badgeClass = "badge-green";
      if (app.status === "Interview") badgeClass = "badge-warning";
      if (app.status === "Rejected") badgeClass = "badge-danger";

      tableHtml += `
        <tr>
          <td><span class="fw-bold text-dark">${app.jobTitle}</span></td>
          <td>${app.company}</td>
          <td class="text-muted small">${app.appliedDate}</td>
          <td><span class="badge ${badgeClass}">${app.status}</span></td>
          <td>
            <button class="btn btn-sm btn-outline-custom" onclick="ApplicationsPage.openStatusModal('${app.jobTitle}', '${app.company}', '${app.status}')">
              Track Status <i class="bi bi-chevron-right ms-1"></i>
            </button>
          </td>
        </tr>
      `;

      mobileHtml += `
        <div class="card-custom mb-3 p-3">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <div>
              <h6 class="fw-bold mb-1">${app.jobTitle}</h6>
              <div class="text-muted small">${app.company}</div>
            </div>
            <span class="badge ${badgeClass}">${app.status}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center text-muted small mt-3 pt-2 border-top">
            <span>Applied: ${app.appliedDate}</span>
            <button class="btn btn-sm btn-primary-custom" onclick="ApplicationsPage.openStatusModal('${app.jobTitle}', '${app.company}', '${app.status}')">Track</button>
          </div>
        </div>
      `;
    });

    tbody.innerHTML = tableHtml;
    container.innerHTML = mobileHtml;
  },

  openStatusModal(title, company, status) {
    document.getElementById("trackerModalTitle").textContent = title;
    document.getElementById("trackerModalCompany").textContent = company;

    const steps = ["Applied", "Under Review", "Shortlisted", "Interview", "Selected"];
    const currentIdx = steps.indexOf(status) !== -1 ? steps.indexOf(status) : 1;

    const timeline = document.getElementById("modalStatusTimeline");
    let html = "";
    steps.forEach((step, i) => {
      let stepClass = "";
      if (i < currentIdx) stepClass = "completed";
      if (i === currentIdx) stepClass = "active";

      html += `
        <div class="timeline-step ${stepClass}">
          <div class="timeline-circle">${i + 1}</div>
          <div class="timeline-label">${step}</div>
        </div>
      `;
    });

    timeline.innerHTML = html;

    const modal = new bootstrap.Modal(document.getElementById("applicationTrackerModal"));
    modal.show();
  }
};
