/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Job Discovery & Career Gateway Engine
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("careerGatewayView")) {
    CareerPage.init();
  }
});

const CareerPage = {
  currentJobs: [],
  selectedJob: null,

  async init() {
    this.bindSearchAndFilters();
    await this.loadJobs();
  },

  async loadJobs(filters = {}) {
    this.currentJobs = await API.getJobs(filters);
    this.renderJobCards();
  },

  renderJobCards() {
    const container = document.getElementById("jobsContainer");
    const countText = document.getElementById("jobCountText");

    if (!container) return;

    if (countText) countText.textContent = `${this.currentJobs.length} Jobs Found`;

    if (this.currentJobs.length === 0) {
      container.innerHTML = `
        <div class="col-12">
          <div class="empty-state card-custom">
            <i class="bi bi-briefcase empty-state-icon"></i>
            <div class="empty-state-title">No Matching Jobs Found</div>
            <div class="empty-state-desc">Try modifying your search criteria or filters to explore more career opportunities.</div>
            <button class="btn btn-outline-custom" onclick="CareerPage.resetFilters()">Reset Filters</button>
          </div>
        </div>
      `;
      return;
    }

    let html = "";
    this.currentJobs.forEach(job => {
      const skillsBadges = job.skillsRequired.map(s => `<span class="badge badge-purple">${s}</span>`).join(" ");
      html += `
        <div class="col-lg-6 col-xl-4 mb-4">
          <div class="job-card">
            <div>
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div class="job-company-logo">
                  <i class="bi bi-building"></i>
                </div>
                <span class="badge badge-green">${job.type}</span>
              </div>
              <h5 class="fw-bold text-dark mb-1">${job.title}</h5>
              <div class="text-muted small mb-2"><i class="bi bi-building me-1"></i>${job.company} • <i class="bi bi-geo-alt me-1"></i>${job.location}</div>
              <div class="fw-bold text-primary mb-3">${job.salary}</div>
              <div class="job-tags mb-3">${skillsBadges}</div>
            </div>
            <div class="d-flex gap-2 border-top pt-3">
              <button class="btn btn-outline-custom btn-sm flex-grow-1" onclick="CareerPage.openJobDetails('${job.id}')">View Details</button>
              <button class="btn btn-primary-custom btn-sm flex-grow-1" onclick="CareerPage.openApplyModal('${job.id}')">Apply Now</button>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  bindSearchAndFilters() {
    const searchInput = document.getElementById("jobSearchInput");
    const locInput = document.getElementById("jobLocationFilter");
    const typeInput = document.getElementById("jobTypeFilter");

    const triggerFilter = () => {
      const filters = {
        search: searchInput ? searchInput.value.trim() : "",
        location: locInput ? locInput.value.trim() : "",
        type: typeInput ? typeInput.value : ""
      };
      this.loadJobs(filters);
    };

    if (searchInput) searchInput.addEventListener("input", triggerFilter);
    if (locInput) locInput.addEventListener("change", triggerFilter);
    if (typeInput) typeInput.addEventListener("change", triggerFilter);
  },

  resetFilters() {
    document.getElementById("jobSearchInput").value = "";
    document.getElementById("jobLocationFilter").value = "";
    document.getElementById("jobTypeFilter").value = "";
    this.loadJobs();
  },

  openJobDetails(jobId) {
    const job = this.currentJobs.find(j => j.id === jobId);
    if (!job) return;
    this.selectedJob = job;

    document.getElementById("modalJobTitle").textContent = job.title;
    document.getElementById("modalJobCompany").textContent = job.company;
    document.getElementById("modalJobLocation").textContent = job.location;
    document.getElementById("modalJobSalary").textContent = job.salary;
    document.getElementById("modalJobType").textContent = job.type;
    document.getElementById("modalJobExperience").textContent = job.experience;
    document.getElementById("modalJobDescription").textContent = job.description;

    const modal = new bootstrap.Modal(document.getElementById("jobDetailsModal"));
    modal.show();
  },

  openApplyModal(jobId) {
    const job = this.currentJobs.find(j => j.id === jobId);
    if (!job) return;
    this.selectedJob = job;

    document.getElementById("applyModalJobTitle").textContent = job.title;
    document.getElementById("applyModalCompany").textContent = job.company;

    const modal = new bootstrap.Modal(document.getElementById("jobApplyModal"));
    modal.show();
  },

  async submitApplication() {
    if (!this.selectedJob) return;
    const user = API.getCurrentUser() || { id: "usr_student_01" };

    try {
      await API.applyJob(user.id, this.selectedJob.id);
      App.showToast(`Application submitted successfully for ${this.selectedJob.title}!`, "success");
      
      const modalElem = document.getElementById("jobApplyModal");
      const modal = bootstrap.Modal.getInstance(modalElem);
      if (modal) modal.hide();

    } catch (err) {
      App.showToast(err.message, "warning");
    }
  }
};
