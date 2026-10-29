/**
 * SMART MOCK TEST & CAREER GATEWAY
 * IndiaBIX-Inspired Comprehensive Mock Test & Practice Portal
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("careerGatewayView")) {
    CareerPage.init();
  }
});

const CareerPage = {
  categories: [],
  allTopics: [],
  activeCategory: null,
  filteredTopics: [],
  studentResults: [],
  studentPracticeResults: [],
  selectedTopic: null,
  selectedMode: "practice", // 'practice' | 'timed'
  selectedDifficulty: "Mixed",
  selectedLength: 5,

  // Job board state
  allJobs: [],
  filteredJobs: [],
  selectedJob: null,

  async init() {
    this.bindViewTabs();
    this.bindPortalSearch();
    this.bindTopicFilters();
    this.bindJobFilters();
    await this.loadStudentPerformance();
    await this.loadData();
    await this.handleUrlParams();
    await this.loadJobs();
  },

  bindViewTabs() {
    const params = new URLSearchParams(window.location.search);
    if (params.get("tab") === "jobs") {
      this.switchView("jobs");
    }
  },

  switchView(viewName) {
    const tabTests = document.getElementById("tabBtnMockTests");
    const tabJobs = document.getElementById("tabBtnJobBoard");
    const sectionTests = document.getElementById("viewMockTestsSection");
    const sectionJobs = document.getElementById("viewJobBoardSection");

    if (viewName === "jobs") {
      tabTests?.classList.remove("active");
      tabJobs?.classList.add("active");
      if (sectionTests) sectionTests.style.display = "none";
      if (sectionJobs) sectionJobs.style.display = "block";
    } else {
      tabJobs?.classList.remove("active");
      tabTests?.classList.add("active");
      if (sectionJobs) sectionJobs.style.display = "none";
      if (sectionTests) sectionTests.style.display = "block";
    }
  },

  async loadStudentPerformance() {
    const user = API.getCurrentUser();
    try {
      this.studentResults = await API.getUserResults(user.id);
      this.studentPracticeResults = await API.getUserPracticeResults(user.id);

      const totalAttempts = this.studentResults.length;
      if (totalAttempts > 0) {
        const validScores = this.studentResults.map(r => { const s = Number(r.scorePct ?? r.percentage ?? r.score); return isNaN(s) || !isFinite(s) ? null : s; }).filter(s => s !== null);
        const totalPct = validScores.reduce((acc, s) => acc + s, 0);
        const avg = validScores.length > 0 ? Math.round(totalPct / validScores.length) : 0;
        const statAvg = document.getElementById("statStudentAvgScore");
        const statAtt = document.getElementById("statStudentAttemptCount");
        if (statAvg) statAvg.textContent = `${avg}%`;
        if (statAtt) statAtt.textContent = `${totalAttempts} Exams Completed`;
      }
    } catch (e) {
      console.warn("[CareerPage] Failed to load student performance:", e);
    }
  },

  async loadData() {
    this.categories = await API.getCategories();
    this.allTopics = await API.getSubjects();

    const statTopics = document.getElementById("statTotalTopicsCount");
    if (statTopics) statTopics.textContent = this.allTopics.length;

    const allQs = JSON.parse(localStorage.getItem("smt_questions") || "[]");
    const statQ = document.getElementById("statTotalQuestionsCount");
    if (statQ) statQ.textContent = `${allQs.length}+`;

    const badgeCat = document.getElementById("badgeTotalCategories");
    if (badgeCat) badgeCat.textContent = this.categories.length;

    this.renderCategoriesGrid();
  },

  async handleUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const catParam = params.get("category");
    const topicParam = params.get("topic");
    const modeParam = params.get("mode");

    if (catParam) {
      const matchedCat = this.categories.find(c => 
        String(c.id).toLowerCase() === catParam.toLowerCase() || 
        String(c.slug).toLowerCase() === catParam.toLowerCase()
      );
      if (matchedCat) {
        this.openCategory(matchedCat.id);
      }
    }

    if (topicParam) {
      const matchedTopic = this.allTopics.find(t => 
        String(t.id).toLowerCase() === topicParam.toLowerCase() || 
        String(t.code).toLowerCase() === topicParam.toLowerCase()
      );
      if (matchedTopic) {
        this.openTopicConfig(matchedTopic.id, modeParam || "practice");
      }
    }
  },

  // ==========================================
  // VIEW 1: 14 MAJOR CATEGORIES HUB
  // ==========================================
  renderCategoriesGrid(filterQuery = "") {
    const container = document.getElementById("categoriesGridContainer");
    if (!container) return;

    let list = this.categories;
    const q = filterQuery.toLowerCase().trim();

    if (q) {
      list = list.filter(cat => 
        cat.name.toLowerCase().includes(q) || 
        cat.description.toLowerCase().includes(q) ||
        this.allTopics.some(t => 
          (t.category_id === cat.id || t.category === cat.name) && 
          (t.name.toLowerCase().includes(q) || (t.topics && t.topics.some(sub => sub.toLowerCase().includes(q))))
        )
      );
    }

    let html = "";
    list.forEach(cat => {
      // Find top 4 topics for preview
      const catTopics = this.allTopics.filter(t => t.category_id === cat.id || t.category === cat.name);
      const previewChips = catTopics.slice(0, 4).map(t => 
        `<span class="category-preview-tag">${t.name}</span>`
      ).join(" ");

      const totalQ = cat.total_questions || catTopics.reduce((acc, t) => acc + (t.question_count || t.questionCount || 0), 0);
      const topicCount = catTopics.length || cat.topic_count || 0;

      html += `
        <div class="col-md-6 col-xl-4">
          <div class="category-portal-card" onclick="CareerPage.openCategory('${cat.id}')">
            <div>
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div class="category-portal-icon" style="background-color: ${cat.bgColor || '#EEECFF'}; color: ${cat.color || 'var(--primary)'};">
                  <i class="bi ${cat.icon || 'bi-journal-code'}"></i>
                </div>
                <span class="badge" style="background-color: ${cat.bgColor || '#EEECFF'}; color: ${cat.color || 'var(--primary)'}; font-weight: 700;">
                  ${topicCount} Topics
                </span>
              </div>

              <h5 class="fw-bold text-dark mb-1">${cat.name}</h5>
              <p class="text-muted small mb-3" style="font-size: 0.825rem; line-height: 1.4; min-height: 2.5rem;">
                ${cat.description}
              </p>

              <div class="category-preview-tags mb-3">
                ${previewChips}
                ${catTopics.length > 4 ? `<span class="category-preview-tag text-primary fw-bold">+${catTopics.length - 4} more</span>` : ''}
              </div>
            </div>

            <div class="d-flex justify-content-between align-items-center pt-3 border-top flex-wrap gap-2">
              <span class="small text-muted">
                <i class="bi bi-patch-check-fill text-success me-1"></i><strong>${totalQ}</strong> MCQs Available
              </span>
              <span class="text-primary fw-semibold small">
                Explore Topics <i class="bi bi-arrow-right"></i>
              </span>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  bindPortalSearch() {
    const searchInput = document.getElementById("globalPortalSearch");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        const val = e.target.value.trim();
        this.renderCategoriesGrid(val);
      });
    }
  },

  showCategoriesHub() {
    this.activeCategory = null;
    document.getElementById("categoriesHubView").style.display = "block";
    document.getElementById("categoryTopicsView").style.display = "none";
    document.getElementById("practiceRunnerView").style.display = "none";
    window.scrollTo({ top: 0, behavior: "smooth" });
  },

  // ==========================================
  // VIEW 2: CATEGORY TOPICS LISTING
  // ==========================================
  openCategory(categoryId) {
    const cat = this.categories.find(c => c.id === categoryId || c.slug === categoryId);
    if (!cat) return;
    this.activeCategory = cat;

    // Update banner & breadcrumb
    document.getElementById("catBreadcrumbCurrent").textContent = cat.name;
    document.getElementById("catBannerTitle").textContent = cat.name;
    document.getElementById("catBannerDesc").textContent = cat.description;
    
    const bannerIcon = document.getElementById("catBannerIcon");
    if (bannerIcon) {
      bannerIcon.style.backgroundColor = cat.bgColor || "#EEECFF";
      bannerIcon.style.color = cat.color || "var(--primary)";
      bannerIcon.innerHTML = `<i class="bi ${cat.icon || 'bi-journal-code'}"></i>`;
    }

    // Switch view
    document.getElementById("categoriesHubView").style.display = "none";
    document.getElementById("categoryTopicsView").style.display = "block";
    document.getElementById("practiceRunnerView").style.display = "none";

    this.applyTopicFilters();
    window.scrollTo({ top: 0, behavior: "smooth" });
  },

  bindTopicFilters() {
    document.getElementById("topicSearchInput")?.addEventListener("input", () => this.applyTopicFilters());
    document.getElementById("topicDifficultyFilter")?.addEventListener("change", () => this.applyTopicFilters());
    document.getElementById("topicAvailabilityFilter")?.addEventListener("change", () => this.applyTopicFilters());
  },

  applyTopicFilters() {
    if (!this.activeCategory) return;

    const search = (document.getElementById("topicSearchInput")?.value || "").toLowerCase().trim();
    const diff = document.getElementById("topicDifficultyFilter")?.value || "";
    const avail = document.getElementById("topicAvailabilityFilter")?.value || "";

    let topics = this.allTopics.filter(t => 
      t.category_id === this.activeCategory.id || t.category === this.activeCategory.name
    );

    const badgeCount = document.getElementById("catBannerTopicCount");
    if (badgeCount) badgeCount.textContent = `${topics.length} Topics`;

    if (search) {
      topics = topics.filter(t => 
        t.name.toLowerCase().includes(search) || 
        (t.code && t.code.toLowerCase().includes(search)) ||
        (t.description && t.description.toLowerCase().includes(search)) ||
        (t.topics && t.topics.some(sub => sub.toLowerCase().includes(search)))
      );
    }

    if (diff) {
      topics = topics.filter(t => (t.difficulty || "Medium").toLowerCase() === diff.toLowerCase());
    }

    if (avail === "ready") {
      topics = topics.filter(t => (t.question_count || t.questionCount || 0) > 0);
    } else if (avail === "coming_soon") {
      topics = topics.filter(t => (t.question_count || t.questionCount || 0) === 0);
    }

    this.filteredTopics = topics;
    this.renderTopicsGrid();
  },

  renderTopicsGrid() {
    const container = document.getElementById("topicsGridContainer");
    const countText = document.getElementById("topicListResultsCount");
    if (!container) return;

    if (countText) {
      countText.textContent = `Showing ${this.filteredTopics.length} Topics in ${this.activeCategory ? this.activeCategory.name : 'Category'}`;
    }

    if (this.filteredTopics.length === 0) {
      container.innerHTML = `
        <div class="col-12">
          <div class="card-custom p-5 text-center">
            <i class="bi bi-search display-4 text-muted mb-3"></i>
            <h5 class="fw-bold text-dark">No Topics Match Your Search</h5>
            <p class="text-muted small">Try modifying your keyword or clearing active difficulty filters.</p>
            <button class="btn btn-outline-custom mt-2" onclick="CareerPage.resetTopicFilters()">
              <i class="bi bi-arrow-counterclockwise me-1"></i> Reset Filters
            </button>
          </div>
        </div>
      `;
      return;
    }

    let html = "";
    this.filteredTopics.forEach(topic => {
      const qCount = topic.question_count ?? topic.questionCount ?? 0;
      const isReady = qCount > 0;
      const isCompany = topic.category_id === "cat_company" || topic.category === "Company-Wise Placement Tests";

      const syllabusChips = (topic.topics || []).slice(0, 3).map(s => 
        `<span class="topic-tag">${s}</span>`
      ).join(" ");

      // Check student best score for this topic
      const bestScore = this.getTopicBestScore(topic.id, topic.name);

      html += `
        <div class="col-md-6 col-xl-4">
          <div class="subject-card-enhanced ${!isReady ? 'opacity-85' : ''}">
            <div>
              <div class="d-flex justify-content-between align-items-start gap-2 mb-2 min-w-0">
                <div class="d-flex align-items-start gap-2 min-w-0 flex-grow-1">
                  <div class="subject-icon-box flex-shrink-0" style="background-color: ${this.activeCategory.bgColor || '#EEECFF'}; color: ${this.activeCategory.color || 'var(--primary)'};">
                    <i class="bi ${topic.icon || 'bi-journal-code'}"></i>
                  </div>
                  <div class="min-w-0 flex-grow-1">
                    <h6 class="fw-bold text-dark mb-1 topic-card-title">${topic.name}</h6>
                    <span class="badge badge-secondary topic-card-badge" style="font-size: 0.7rem;">${topic.code || 'TOPIC'}</span>
                  </div>
                </div>
                ${isCompany ? `<span class="badge-pyq-notice flex-shrink-0"><i class="bi bi-patch-check-fill"></i> PYQ-Style</span>` : ''}
              </div>

              <p class="text-muted small mb-2" style="font-size: 0.8rem; min-height: 2.2rem; line-height: 1.3;">
                ${topic.description || 'Topic fundamentals, conceptual problem solving, and placement MCQs.'}
              </p>

              <div class="topics-pill-list mb-3">
                ${syllabusChips}
                ${(topic.topics && topic.topics.length > 3) ? `<span class="topic-tag text-primary fw-bold">+${topic.topics.length - 3}</span>` : ''}
              </div>
            </div>

            <div>
              <div class="card-meta-bar mb-3">
                <span>
                  <i class="bi ${isReady ? 'bi-check-circle-fill text-success' : 'bi-hourglass-split text-warning'} me-1"></i>
                  <strong class="${isReady ? 'text-dark' : 'text-muted'}">${isReady ? `${qCount} MCQs` : 'Coming Soon'}</strong>
                </span>
                <span><i class="bi bi-clock me-1"></i>${topic.defaultDuration || 25} mins</span>
                <span class="badge badge-${(topic.difficulty || 'Medium') === 'Easy' ? 'success' : (topic.difficulty || 'Medium') === 'Hard' ? 'danger' : 'purple'}">
                  ${topic.difficulty || 'Medium'}
                </span>
              </div>

              ${bestScore !== null ? `
                <div class="d-flex justify-content-between align-items-center bg-surface-subtle p-2 rounded small mb-3 border">
                  <span class="text-muted small"><i class="bi bi-trophy-fill text-warning me-1"></i>Best Score:</span>
                  <span class="fw-bold text-success">${bestScore}%</span>
                </div>
              ` : ''}

              <!-- Dual Buttons: Practice Mode vs Timed Test -->
              ${isReady ? `
                <div class="d-flex gap-2 flex-wrap">
                  <button type="button" class="btn btn-outline-custom btn-sm flex-fill" onclick="CareerPage.openTopicConfig('${topic.id}', 'practice')">
                    <i class="bi bi-mortarboard-fill me-1 text-primary"></i> Practice
                  </button>
                  <button type="button" class="btn btn-primary-custom btn-sm flex-fill" onclick="CareerPage.openTopicConfig('${topic.id}', 'timed')">
                    <i class="bi bi-clock-history me-1"></i> Timed Test
                  </button>
                </div>
              ` : `
                <button type="button" class="btn btn-outline-custom w-100 btn-sm text-muted" onclick="CareerPage.openComingSoonModal('${topic.id}')">
                  <i class="bi bi-info-circle me-1"></i> Questions Coming Soon
                </button>
              `}
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  getTopicBestScore(topicId, topicName) {
    const matching = this.studentResults.filter(r => 
      String(r.subjectId || "").toLowerCase() === String(topicId).toLowerCase() || 
      String(r.subjectName || "").toLowerCase() === String(topicName).toLowerCase()
    );
    if (matching.length === 0) return null;
    return Math.max(...matching.map(r => r.scorePct || r.percentage || 0));
  },

  resetTopicFilters() {
    const s = document.getElementById("topicSearchInput");
    if (s) s.value = "";
    const d = document.getElementById("topicDifficultyFilter");
    if (d) d.value = "";
    const a = document.getElementById("topicAvailabilityFilter");
    if (a) a.value = "";
    this.applyTopicFilters();
  },

  filterOnlyReady() {
    const csModal = bootstrap.Modal.getInstance(document.getElementById("comingSoonModal"));
    if (csModal) csModal.hide();
    const a = document.getElementById("topicAvailabilityFilter");
    if (a) a.value = "ready";
    this.applyTopicFilters();
  },

  // ==========================================
  // VIEW 3: TOPIC CONFIGURATION MODAL
  // ==========================================
  openTopicConfig(topicId, defaultMode = "practice") {
    const topic = this.allTopics.find(t => t.id === topicId);
    if (!topic) return;
    this.selectedTopic = topic;

    // Reset default selections
    this.selectedMode = defaultMode;
    this.selectedDifficulty = "Mixed";
    this.selectedLength = 5;

    document.getElementById("modalTopicName").textContent = topic.name;
    document.getElementById("modalTopicCategory").textContent = topic.category || "General";
    document.getElementById("modalTopicDesc").textContent = topic.description || "";

    const iconBox = document.getElementById("modalTopicIcon");
    if (iconBox) {
      iconBox.innerHTML = `<i class="bi ${topic.icon || 'bi-journal-code'}"></i>`;
    }

    // Company notice
    const isCompany = topic.category_id === "cat_company" || topic.category === "Company-Wise Placement Tests";
    const compNotice = document.getElementById("modalTopicCompanyNotice");
    if (compNotice) {
      if (isCompany) compNotice.style.setProperty("display", "flex", "important");
      else compNotice.style.setProperty("display", "none", "important");
    }

    // Syllabus
    const syllabusList = document.getElementById("modalTopicTopicsList");
    if (syllabusList) {
      syllabusList.innerHTML = (topic.topics || []).map(s => `<span class="topic-tag">${s}</span>`).join(" ");
    }

    // Past Score
    const bestScore = this.getTopicBestScore(topic.id, topic.name);
    const histText = document.getElementById("modalTopicHistoryText");
    const histBadge = document.getElementById("modalTopicHistoryBadge");
    if (bestScore !== null) {
      if (histText) histText.textContent = `Highest Score: ${bestScore}% recorded`;
      if (histBadge) histBadge.innerHTML = `<span class="badge bg-success">Best: ${bestScore}%</span>`;
    } else {
      if (histText) histText.textContent = "No previous attempts recorded";
      if (histBadge) histBadge.innerHTML = `<span class="badge bg-secondary">Fresh Session</span>`;
    }

    // Select mode UI
    this.selectMode(defaultMode);

    // Difficulty selection cards
    const diffCards = document.querySelectorAll("#modalTopicDifficultyGroup .config-option-card");
    diffCards.forEach(c => {
      const dVal = c.getAttribute("data-diff");
      if (dVal === "Mixed") c.classList.add("selected");
      else c.classList.remove("selected");

      c.onclick = () => {
        diffCards.forEach(x => x.classList.remove("selected"));
        c.classList.add("selected");
        this.selectedDifficulty = dVal;
      };
    });

    // Length selection cards
    const qCount = topic.question_count ?? topic.questionCount ?? 0;
    const allText = document.getElementById("modalTopicLengthAllText");
    if (allText) allText.textContent = `All Available Questions (${qCount} Qs)`;

    const lenCards = document.querySelectorAll("#modalTopicLengthGroup .config-option-card");
    lenCards.forEach(c => {
      const lVal = c.getAttribute("data-len");
      if (lVal === "5") c.classList.add("selected");
      else c.classList.remove("selected");

      c.onclick = () => {
        lenCards.forEach(x => x.classList.remove("selected"));
        c.classList.add("selected");
        this.selectedLength = lVal === "all" ? qCount : parseInt(lVal, 10);
      };
    });

    // Launch button handler
    const btnLaunch = document.getElementById("btnLaunchTopicSession");
    if (btnLaunch) {
      btnLaunch.onclick = () => {
        const modalEl = document.getElementById("topicConfigModal");
        const modalInst = bootstrap.Modal.getInstance(modalEl);
        if (modalInst) modalInst.hide();

        if (this.selectedMode === "practice") {
          // Launch in-portal interactive practice session
          PracticeEngine.start(this.selectedTopic, this.selectedDifficulty, this.selectedLength);
        } else {
          // Launch timed proctored exam
          const url = `mock-test.html?subject=${encodeURIComponent(this.selectedTopic.id)}&difficulty=${encodeURIComponent(this.selectedDifficulty)}&length=${this.selectedLength}&mode=timed`;
          window.location.href = url;
        }
      };
    }

    const modal = new bootstrap.Modal(document.getElementById("topicConfigModal"));
    modal.show();
  },

  selectMode(mode) {
    this.selectedMode = mode;
    const cardPractice = document.getElementById("modeCardPractice");
    const cardTimed = document.getElementById("modeCardTimed");
    const launchBtn = document.getElementById("btnLaunchTopicSession");

    if (mode === "practice") {
      cardPractice?.classList.add("selected");
      cardTimed?.classList.remove("selected");
      if (launchBtn) launchBtn.innerHTML = `Start Practice Session <i class="bi bi-mortarboard-fill ms-1"></i>`;
    } else {
      cardTimed?.classList.add("selected");
      cardPractice?.classList.remove("selected");
      if (launchBtn) launchBtn.innerHTML = `Launch Timed Mock Exam <i class="bi bi-clock-history ms-1"></i>`;
    }
  },

  openComingSoonModal(topicId) {
    const topic = this.allTopics.find(t => t.id === topicId);
    if (!topic) return;

    document.getElementById("csSubjectName").textContent = topic.name;
    document.getElementById("csSubjectCategory").textContent = `Category: ${topic.category || 'General'}`;

    const topicsList = document.getElementById("csTopicsList");
    if (topicsList) {
      topicsList.innerHTML = (topic.topics || []).map(s => `<span class="topic-tag">${s}</span>`).join(" ");
    }

    const modal = new bootstrap.Modal(document.getElementById("comingSoonModal"));
    modal.show();
  },

  // ==========================================
  // PRESERVED PLACEMENT JOBS FUNCTIONS
  // ==========================================
  async loadJobs(filters = {}) {
    this.allJobs = await API.getJobs(filters);
    this.filteredJobs = this.allJobs;

    const badge = document.getElementById("badgeTotalJobs");
    if (badge) badge.textContent = this.allJobs.length;

    this.renderJobCards();
  },

  renderJobCards() {
    const container = document.getElementById("jobsContainer");
    const countText = document.getElementById("jobCountText");
    if (!container) return;

    if (countText) countText.textContent = `${this.filteredJobs.length} Jobs Found`;

    if (this.filteredJobs.length === 0) {
      container.innerHTML = `
        <div class="col-12">
          <div class="card-custom p-5 text-center">
            <i class="bi bi-briefcase display-4 text-muted mb-3"></i>
            <h5 class="fw-bold text-dark">No Matching Jobs Found</h5>
            <p class="text-muted small">Try modifying your search criteria or resetting filters.</p>
            <button class="btn btn-outline-custom mt-2" onclick="CareerPage.resetJobFilters()">Reset Filters</button>
          </div>
        </div>
      `;
      return;
    }

    let html = "";
    this.filteredJobs.forEach(job => {
      const skillsBadges = (job.skillsRequired || []).map(s => `<span class="badge badge-purple">${s}</span>`).join(" ");
      html += `
        <div class="col-lg-6 col-xl-4 mb-4">
          <div class="job-card">
            <div>
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div class="job-company-logo"><i class="bi bi-building"></i></div>
                <span class="badge badge-green">${job.type}</span>
              </div>
              <h5 class="fw-bold text-dark mb-1">${job.title}</h5>
              <div class="text-muted small mb-2"><i class="bi bi-building me-1"></i>${job.company} • <i class="bi bi-geo-alt me-1"></i>${job.location}</div>
              <div class="fw-bold text-primary mb-3">${job.salary}</div>
              <div class="job-tags mb-3">${skillsBadges}</div>
            </div>
            <div class="d-flex gap-2 border-top pt-3 flex-wrap">
              <button class="btn btn-outline-custom btn-sm flex-grow-1" onclick="CareerPage.openJobDetails('${job.id}')">View Details</button>
              <button class="btn btn-primary-custom btn-sm flex-grow-1" onclick="CareerPage.openApplyModal('${job.id}')">Apply Now</button>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  bindJobFilters() {
    const searchInput = document.getElementById("jobSearchInput");
    const locInput = document.getElementById("jobLocationFilter");
    const typeInput = document.getElementById("jobTypeFilter");

    const trigger = () => {
      const filters = {
        search: searchInput ? searchInput.value.trim() : "",
        location: locInput ? locInput.value.trim() : "",
        type: typeInput ? typeInput.value : ""
      };
      this.loadJobs(filters);
    };

    if (searchInput) searchInput.addEventListener("input", trigger);
    if (locInput) locInput.addEventListener("change", trigger);
    if (typeInput) typeInput.addEventListener("change", trigger);
  },

  resetJobFilters() {
    const s = document.getElementById("jobSearchInput");
    if (s) s.value = "";
    const l = document.getElementById("jobLocationFilter");
    if (l) l.value = "";
    const t = document.getElementById("jobTypeFilter");
    if (t) t.value = "";
    this.loadJobs();
  },

  openJobDetails(jobId) {
    const job = this.filteredJobs.find(j => j.id === jobId);
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
    const job = this.filteredJobs.find(j => j.id === jobId);
    if (!job) return;
    this.selectedJob = job;

    document.getElementById("applyModalJobTitle").textContent = job.title;
    document.getElementById("applyModalCompany").textContent = job.company;

    const modal = new bootstrap.Modal(document.getElementById("jobApplyModal"));
    modal.show();
  },

  async submitApplication() {
    if (!this.selectedJob) return;
    const user = API.getCurrentUser();

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

/**
 * Interactive Self-Paced Practice Engine
 * Instant feedback, step-by-step explanations, non-proctored learning
 */
const PracticeEngine = {
  activeTopic: null,
  questions: [],
  currentIndex: 0,
  userAnswers: {}, // { [qId]: selectedOptIdx }
  score: 0,
  answeredCount: 0,

  async start(topic, difficulty, length) {
    this.activeTopic = topic;
    this.currentIndex = 0;
    this.userAnswers = {};
    this.score = 0;
    this.answeredCount = 0;

    // Fetch questions with explanations
    this.questions = await API.getPracticeQuestions(topic.id, difficulty, length);

    if (!this.questions || this.questions.length === 0) {
      App.showToast(`No practice questions found for ${topic.name}.`, "info");
      return;
    }

    // Update practice runner header
    document.getElementById("practiceTopicBadge").textContent = topic.name;
    document.getElementById("practiceDifficultyBadge").textContent = difficulty || "Mixed";
    document.getElementById("practiceRunnerTopicTitle").textContent = `${topic.name} – Self-Paced Practice`;

    // Show Practice view
    document.getElementById("categoriesHubView").style.display = "none";
    document.getElementById("categoryTopicsView").style.display = "none";
    document.getElementById("practiceRunnerView").style.display = "block";

    this.renderCurrentQuestion();
    window.scrollTo({ top: 0, behavior: "smooth" });
  },

  renderCurrentQuestion() {
    const q = this.questions[this.currentIndex];
    if (!q) return;

    // Progress
    const total = this.questions.length;
    const currentNum = this.currentIndex + 1;
    document.getElementById("practiceQuestionProgressText").textContent = `Question ${currentNum} of ${total}`;
    
    const pct = Math.round((currentNum / total) * 100);
    const pBar = document.getElementById("practiceProgressBar");
    if (pBar) pBar.style.width = `${pct}%`;

    // Score tracker
    document.getElementById("practiceScoreTrackerText").textContent = `Score: ${this.score} / ${this.answeredCount}`;

    // Question Text
    document.getElementById("practiceQuestionText").textContent = q.question_text || q.question;

    // Options
    const optionsContainer = document.getElementById("practiceOptionsContainer");
    const prefixes = ["A", "B", "C", "D"];
    const hasAnswered = this.userAnswers[q.id] !== undefined;
    const selectedOptIdx = this.userAnswers[q.id];

    // Determine correct index (0-3)
    let correctIdx = q.correctIndex;
    if (correctIdx === undefined && q.correct_option) {
      const optMap = { "A": 0, "B": 1, "C": 2, "D": 3 };
      correctIdx = optMap[q.correct_option.toUpperCase()] ?? 0;
    }

    let optionsHtml = "";
    (q.options || [q.option_a, q.option_b, q.option_c, q.option_d]).forEach((optText, idx) => {
      let extraClass = "";
      if (hasAnswered) {
        extraClass = "locked ";
        if (idx === correctIdx) {
          extraClass += "correct";
        } else if (idx === selectedOptIdx) {
          extraClass += "incorrect";
        }
      }

      optionsHtml += `
        <div class="practice-option-item ${extraClass}" data-opt-idx="${idx}" onclick="PracticeEngine.selectOption(${idx})">
          <div class="practice-option-prefix">${prefixes[idx]}</div>
          <div class="flex-grow-1">${optText}</div>
          ${hasAnswered && idx === correctIdx ? '<i class="bi bi-check-circle-fill text-success fs-5"></i>' : ''}
          ${hasAnswered && idx === selectedOptIdx && idx !== correctIdx ? '<i class="bi bi-x-circle-fill text-danger fs-5"></i>' : ''}
        </div>
      `;
    });

    optionsContainer.innerHTML = optionsHtml;

    // Explanation card
    const expCard = document.getElementById("practiceExplanationCard");
    const expText = document.getElementById("practiceExplanationText");
    if (hasAnswered) {
      expCard.style.display = "block";
      expText.textContent = q.explanation || `Correct Answer: Option ${prefixes[correctIdx]}.`;
    } else {
      expCard.style.display = "none";
    }

    // Button states
    document.getElementById("btnPracticePrev").disabled = this.currentIndex === 0;
    const nextBtn = document.getElementById("btnPracticeNext");
    if (this.currentIndex === total - 1) {
      nextBtn.innerHTML = `Finish Practice <i class="bi bi-check2-circle ms-1"></i>`;
    } else {
      nextBtn.innerHTML = `Next Question <i class="bi bi-chevron-right ms-1"></i>`;
    }
  },

  selectOption(optIdx) {
    const q = this.questions[this.currentIndex];
    if (!q || this.userAnswers[q.id] !== undefined) return; // Prevent changing after answer

    this.userAnswers[q.id] = optIdx;
    this.answeredCount++;

    let correctIdx = q.correctIndex;
    if (correctIdx === undefined && q.correct_option) {
      const optMap = { "A": 0, "B": 1, "C": 2, "D": 3 };
      correctIdx = optMap[q.correct_option.toUpperCase()] ?? 0;
    }

    if (optIdx === correctIdx) {
      this.score++;
    }

    this.renderCurrentQuestion();
  },

  prevQuestion() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderCurrentQuestion();
    }
  },

  nextQuestion() {
    if (this.currentIndex < this.questions.length - 1) {
      this.currentIndex++;
      this.renderCurrentQuestion();
    } else {
      this.finishPractice();
    }
  },

  async finishPractice() {
    const total = this.questions.length;
    const accuracy = this.answeredCount > 0 ? Math.round((this.score / this.answeredCount) * 100) : 0;

    // Save record
    const user = API.getCurrentUser();
    await API.savePracticeResult({
      userId: user.id,
      topicId: this.activeTopic ? this.activeTopic.id : "topic",
      topicName: this.activeTopic ? this.activeTopic.name : "Practice Topic",
      score: this.score,
      answeredCount: this.answeredCount,
      totalQuestions: total,
      accuracy
    });

    // Populate summary modal
    document.getElementById("summaryTopicTitle").textContent = this.activeTopic ? this.activeTopic.name : "Practice Session";
    document.getElementById("summaryScore").textContent = `${this.score}/${total}`;
    document.getElementById("summaryAccuracy").textContent = `${accuracy}%`;
    document.getElementById("summaryTotalQ").textContent = total;

    const btnSwitch = document.getElementById("btnSwitchToTimedFromSummary");
    if (btnSwitch) {
      btnSwitch.onclick = () => {
        const modalEl = document.getElementById("practiceSummaryModal");
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
        window.location.href = `mock-test.html?subject=${encodeURIComponent(this.activeTopic.id)}&difficulty=Mixed&length=10&mode=timed`;
      };
    }

    const modal = new bootstrap.Modal(document.getElementById("practiceSummaryModal"));
    modal.show();

    // Exit practice view back to topic list
    this.exitPractice();
  },

  exitPractice() {
    document.getElementById("practiceRunnerView").style.display = "none";
    if (CareerPage.activeCategory) {
      document.getElementById("categoryTopicsView").style.display = "block";
    } else {
      document.getElementById("categoriesHubView").style.display = "block";
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};
