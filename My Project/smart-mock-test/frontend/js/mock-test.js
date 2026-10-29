/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Comprehensive Interactive Mock Test Flow Engine
 * Enhanced with Full-Screen Examination Mode, Anti-Cheating Proctoring & Subject-Wise Tests
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("mockTestAppView")) {
    MockTestEngine.init();
  }
});

const MockTestEngine = {
  currentStep: 1, // 1: Subject, 2: Config/Difficulty, 3: Camera, 4: Test
  selectedSubject: null,
  testSubjectLabel: "",
  selectedDifficulty: "Medium",
  testDifficultyLabel: "Medium",
  selectedLength: 10,
  cameraStream: null,
  testControlsBound: false,
  currentAttemptId: null,
  preTestFaceCheckInterval: null,
  facePresenceVerified: false,
  isSubmitting: false,

  // Catalog State
  allSubjects: [],
  activeCategory: "all",
  searchQuery: "",

  // Test State
  questions: [],
  currentIndex: 0,
  userAnswers: {}, // { qId: optionIndex }
  markedForReview: new Set(),
  timerSeconds: 900, // Dynamic (default 15 mins for 10 Qs)
  initialTimerSeconds: 900,
  timerInterval: null,

  async init() {
    this.bindStepNavigation();
    this.bindCategoryTabs();
    this.bindSearch();
    this.bindLengthSelection();
    this.bindDifficulty();
    this.bindCameraControls();
    await this.loadAndRenderSubjects();
    await this.handleUrlParameters();
  },

  async handleUrlParameters() {
    const urlParams = new URLSearchParams(window.location.search);
    const subParam = urlParams.get("subject");
    const diffParam = urlParams.get("difficulty");
    const lenParam = urlParams.get("length");

    if (diffParam) {
      this.selectedDifficulty = diffParam;
      this.testDifficultyLabel = diffParam;
    }
    if (lenParam) {
      if (lenParam === "max") {
        this.selectedLength = "max";
      } else {
        const parsedLen = parseInt(lenParam, 10);
        if (!isNaN(parsedLen) && parsedLen > 0) {
          this.selectedLength = parsedLen;
        }
      }
    }

    if (subParam) {
      const subjects = this.allSubjects.length > 0 ? this.allSubjects : await API.getSubjects();
      const sParamLower = subParam.toLowerCase();
      const matched = subjects.find(s => 
        String(s.id || "").toLowerCase() === sParamLower || 
        String(s.name || "").toLowerCase() === sParamLower ||
        String(s.code || "").toLowerCase() === sParamLower
      );

      if (matched) {
        this.selectSubject(matched);

        // Check if subject currently has 0 available questions
        const availableQs = await API.getQuestions(matched.id);
        if (availableQs.length === 0 && (matched.question_count || 0) === 0) {
          App.showToast(`Questions coming soon for ${matched.name}. Please select an active subject.`, "info");
          this.goToStep(1);
          return;
        }

        // Fast-track directly to Step 3 (Camera Verification)
        this.goToStep(3);
        App.showToast(`Ready for ${matched.name} (${this.selectedDifficulty} Difficulty). Complete camera check to proceed.`, "info");
      }
    }
  },

  async loadAndRenderSubjects() {
    try {
      this.allSubjects = await API.getSubjects();
    } catch (err) {
      console.warn("[MockTestEngine] Failed to load subjects via API, falling back to mock-data:", err);
      this.allSubjects = (typeof DEFAULT_MOCK_DATA !== "undefined" && DEFAULT_MOCK_DATA.subjects) || [];
    }
    this.renderSubjectCards(this.allSubjects);
  },

  bindCategoryTabs() {
    const tabContainer = document.getElementById("mockCategoryTabs");
    if (!tabContainer) return;

    tabContainer.querySelectorAll("button").forEach(btn => {
      btn.addEventListener("click", () => {
        tabContainer.querySelectorAll("button").forEach(b => {
          b.classList.remove("btn-primary-custom", "active");
          b.classList.add("btn-outline-custom");
        });
        btn.classList.remove("btn-outline-custom");
        btn.classList.add("btn-primary-custom", "active");

        this.activeCategory = btn.getAttribute("data-cat") || "all";
        this.filterAndRenderSubjects();
      });
    });
  },

  bindSearch() {
    const searchInput = document.getElementById("mockSubjectSearch");
    if (!searchInput) return;

    searchInput.addEventListener("input", (e) => {
      this.searchQuery = (e.target.value || "").trim().toLowerCase();
      this.filterAndRenderSubjects();
    });
  },

  filterAndRenderSubjects() {
    let filtered = [...this.allSubjects];

    // Filter by Category
    if (this.activeCategory && this.activeCategory !== "all") {
      filtered = filtered.filter(s => {
        const catId = (s.category_id || "").toLowerCase();
        const catName = (s.category || "").toLowerCase();
        const target = this.activeCategory.toLowerCase();

        if (catId === target) return true;
        if (target === "cat_programming" && (catName.includes("programming") || catId.includes("programming"))) return true;
        if (target === "cat_core_cs" && (catName.includes("core") || catId.includes("core"))) return true;
        if (target === "cat_web_dev" && (catName.includes("web") || catId.includes("web"))) return true;
        if (target === "cat_db_net" && (catName.includes("database") || catName.includes("network") || catId.includes("db"))) return true;
        if (target === "cat_technical_mcqs" && (catName.includes("technical") || catName.includes("emerging") || catId.includes("technical"))) return true;
        if (target === "cat_quant" && (catName.includes("quantitative") || catName.includes("aptitude") || catId.includes("quant") || catId.includes("logical") || catId.includes("verbal"))) return true;
        if (target === "cat_company" && (catName.includes("company") || catName.includes("placement") || catId.includes("company"))) return true;
        return false;
      });
    }

    // Filter by Search Query
    if (this.searchQuery) {
      filtered = filtered.filter(s => {
        const name = (s.name || "").toLowerCase();
        const code = (s.code || "").toLowerCase();
        const cat = (s.category || "").toLowerCase();
        const desc = (s.description || "").toLowerCase();
        const topics = (s.topics || []).join(" ").toLowerCase();
        return name.includes(this.searchQuery) || 
               code.includes(this.searchQuery) || 
               cat.includes(this.searchQuery) || 
               desc.includes(this.searchQuery) ||
               topics.includes(this.searchQuery);
      });
    }

    this.renderSubjectCards(filtered);
  },

  renderSubjectCards(subjects) {
    const container = document.getElementById("subjectGridContainer");
    const badge = document.getElementById("subjectCountBadge");
    if (!container) return;

    if (badge) {
      badge.innerHTML = `<i class="bi bi-collection me-1"></i> Showing ${subjects.length} of ${this.allSubjects.length} Modules`;
    }

    if (subjects.length === 0) {
      container.innerHTML = `
        <div class="col-12 text-center py-5">
          <i class="bi bi-search fs-1 text-muted mb-3 d-block"></i>
          <h6 class="fw-bold text-dark">No matching subjects found</h6>
          <p class="text-muted small">Try searching for keywords like "Python", "DSA", "DBMS", "Java", or "SQL".</p>
        </div>
      `;
      return;
    }

    let html = "";
    subjects.forEach(sub => {
      const qCount = sub.question_count ?? sub.questionCount ?? 0;
      const countLabel = qCount > 0 ? `${qCount} Questions Available` : `Questions Coming Soon`;
      const isComingSoon = qCount === 0;
      const isSelected = this.selectedSubject && this.selectedSubject.id === sub.id;

      html += `
        <div class="subject-card ${isComingSoon ? 'opacity-75' : ''} ${isSelected ? 'selected' : ''}" 
             data-sub-id="${sub.id}" 
             data-sub-name="${sub.name}">
          <div class="subject-card-body">
            <div class="subject-card-header">
              <div class="stat-icon-wrapper stat-icon-purple flex-shrink-0">
                <i class="bi ${sub.icon || 'bi-journal-code'}"></i>
              </div>
              <div class="subject-card-info">
                <h6 class="subject-card-title">${sub.name}</h6>
                <div class="subject-card-badges">
                  <span class="badge badge-secondary small">${sub.category || 'Core CS'}</span>
                  ${sub.code ? `<span class="badge bg-light text-dark border small text-nowrap">${sub.code}</span>` : ''}
                </div>
              </div>
            </div>
            <p class="subject-card-desc mb-0">${sub.description || 'Comprehensive CSE technical module covering conceptual & placement MCQs.'}</p>
          </div>
          <div class="subject-card-footer">
            <span class="subject-card-count ${isComingSoon ? 'text-warning' : 'text-muted'}">
              <i class="bi ${isComingSoon ? 'bi-hourglass-split' : 'bi-check-circle'} me-1 text-success"></i>${countLabel}
            </span>
            <span class="subject-card-action text-primary">${isComingSoon ? 'Coming Soon' : 'Configure Test'} <i class="bi bi-chevron-right"></i></span>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;

        // Card click events: Selecting a card transitions immediately to Test Details (Step 2)
    container.querySelectorAll(".subject-card").forEach(card => {
      card.addEventListener("click", () => {
        const subId = card.getAttribute("data-sub-id");
        const found = this.allSubjects.find(s => s.id === subId);
        if (found) {
          const qCount = found.question_count ?? found.questionCount ?? 0;
          if (qCount === 0) {
            App.showToast(`Questions coming soon for ${found.name}. Please select an active subject.`, "info");
            return;
          }
          this.selectSubject(found);
          this.goToStep(2);
        }
      });
    });
  },

  selectSubject(sub) {
    this.selectedSubject = {
      id: sub.id,
      name: sub.name,
      code: sub.code || "CS",
      category: sub.category || "Core CS",
      category_id: sub.category_id || "cat_core_cs",
      icon: sub.icon || "bi-journal-code",
      defaultDuration: sub.defaultDuration || 30,
      question_count: sub.question_count ?? sub.questionCount ?? 0
    };
    this.testSubjectLabel = sub.name;

    // Highlight card
    document.querySelectorAll(".subject-card").forEach(c => {
      if (c.getAttribute("data-sub-id") === sub.id) {
        c.classList.add("selected");
      } else {
        c.classList.remove("selected");
      }
    });

    // Update feedback
    const feedback = document.getElementById("selectedSubjectFeedback");
    if (feedback) {
      feedback.innerHTML = `<i class="bi bi-check-circle-fill text-success me-1"></i> Selected: <strong>${sub.name}</strong> (${this.selectedSubject.question_count} Questions Available)`;
    }

    const nextBtn = document.getElementById("btnStep1Next");
    if (nextBtn) nextBtn.disabled = false;

    // Populate Step 2 Configuration Elements
    const cfgName = document.getElementById("cfgSubjectName");
    const cfgCat = document.getElementById("cfgSubjectCategory");
    const cfgCode = document.getElementById("cfgSubjectCode");
    const cfgIcon = document.getElementById("cfgSubjectIcon");
    const cfgAvail = document.getElementById("cfgSubjectAvailableCount");
    const cfgMaxLabel = document.getElementById("cfgLenMaxLabel");

    if (cfgName) cfgName.textContent = sub.name;
    if (cfgCat) cfgCat.textContent = sub.category || "Core Computer Science";
    if (cfgCode) cfgCode.textContent = sub.code || "CS-MOD";
    if (cfgIcon) cfgIcon.className = `bi ${sub.icon || "bi-journal-code"} fs-4`;
    if (cfgAvail) cfgAvail.textContent = `${this.selectedSubject.question_count} Questions`;
    if (cfgMaxLabel) cfgMaxLabel.textContent = `All (${this.selectedSubject.question_count} Qs)`;

    this.recalculateConfigTiming();
  },

  bindLengthSelection() {
    const cards = document.querySelectorAll(".cfg-len-card");
    cards.forEach(card => {
      card.addEventListener("click", () => {
        cards.forEach(c => c.classList.remove("selected"));
        card.classList.add("selected");

        const val = card.getAttribute("data-length");
        if (val === "max") {
          this.selectedLength = "max";
        } else {
          this.selectedLength = parseInt(val, 10) || 10;
        }
        this.recalculateConfigTiming();
      });
    });
  },

  bindDifficulty() {
    const cards = document.querySelectorAll(".difficulty-card");
    cards.forEach(card => {
      card.addEventListener("click", () => {
        cards.forEach(c => c.classList.remove("selected"));
        card.classList.add("selected");
        this.selectedDifficulty = card.getAttribute("data-diff") || "Medium";
        this.testDifficultyLabel = this.selectedDifficulty;
      });
    });
  },

  recalculateConfigTiming() {
    const count = this.selectedLength === "max" 
      ? (this.selectedSubject ? this.selectedSubject.question_count : 50)
      : (parseInt(this.selectedLength, 10) || 10);

    const mins = Math.max(10, Math.round(count * 1.5));

    const durationBadge = document.getElementById("cfgDurationBadge");
    const ruleTiming = document.getElementById("cfgRuleTiming");

    if (durationBadge) {
      durationBadge.innerHTML = `<i class="bi bi-clock-history me-1"></i> Duration: ${mins} Mins`;
    }
    if (ruleTiming) {
      ruleTiming.textContent = `Dynamic Duration: ${mins} minutes allocated for ${count} questions (1.5 mins per question).`;
    }
  },

  bindStepNavigation() {
    document.getElementById("btnStep1Next")?.addEventListener("click", () => {
      if (!this.selectedSubject) {
        App.showToast("Please select a subject module first.", "warning");
        return;
      }
      this.goToStep(2);
    });

    const startTestFromStep2 = () => {
      if (!this.selectedSubject) {
        App.showToast("Please select a subject module first.", "warning");
        return;
      }
      this.goToStep(3);
    };

    // Step 2 Navigation: Back to Mock Tests
    document.getElementById("btnStep2Back")?.addEventListener("click", () => this.goToStep(1));
    document.getElementById("btnStep2BackTop")?.addEventListener("click", () => this.goToStep(1));

    // Step 2 Action: Start Test (Top, Summary Banner, and Bottom)
    document.getElementById("btnStep2Next")?.addEventListener("click", startTestFromStep2);
    document.getElementById("btnStep2StartTop")?.addEventListener("click", startTestFromStep2);
    document.getElementById("btnStep2QuickStart")?.addEventListener("click", startTestFromStep2);
    document.getElementById("btnStep3Back")?.addEventListener("click", () => {
      if (this.preTestFaceCheckInterval) {
        clearInterval(this.preTestFaceCheckInterval);
        this.preTestFaceCheckInterval = null;
      }
      this.goToStep(2);
    });

    document.getElementById("btnStep3Next")?.addEventListener("click", async () => {
      if (!this.hasActiveCamera()) {
        App.showToast("An active camera is required to continue.", "error");
        return;
      }

      if (!this.facePresenceVerified) {
        App.showToast("Face verification required before launching test. Please center your face in the camera view.", "warning");
        return;
      }

      await this.startActualTest();
    });
  },

  hasActiveCamera() {
    return Boolean(this.cameraStream && this.cameraStream.getVideoTracks().some(track => (
      track.enabled && track.readyState === "live"
    )));
  },

  bindCameraControls() {
    const enableBtn = document.getElementById("btnEnableCamera");
    const videoElem = document.getElementById("cameraVideoFeed");
    const statusText = document.getElementById("cameraStatusText");
    const fallback = document.getElementById("cameraFallbackPlaceholder");
    const nextBtn = document.getElementById("btnStep3Next");

    if (!enableBtn || !videoElem || !statusText || !fallback || !nextBtn) return;

    enableBtn.addEventListener("click", async () => {
      if (this.hasActiveCamera()) return;

      enableBtn.disabled = true;
      statusText.innerHTML = '<i class="bi bi-circle-fill text-warning me-1"></i> Requesting camera permission...';
      statusText.classList.remove("bg-danger", "bg-success");
      statusText.classList.add("bg-dark");

      try {
        if (!navigator.mediaDevices?.getUserMedia) {
          throw new Error("Camera access is unavailable in this browser.");
        }

        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        const videoTrack = stream.getVideoTracks().find(track => track.enabled && track.readyState === "live");
        if (!videoTrack) {
          stream.getTracks().forEach(track => track.stop());
          throw new Error("No active camera track was provided.");
        }

        this.cameraStream = stream;
        videoElem.srcObject = stream;
        videoElem.style.display = "block";
        fallback.style.display = "none";

        videoTrack.addEventListener("ended", () => this.handleCameraLoss());

        // Wait for video frame to begin playing before starting face analysis
        await new Promise(resolve => {
          if (videoElem.readyState >= 2) resolve();
          else videoElem.onloadeddata = () => resolve();
        });
        videoElem.play().catch(() => {});

        this.startPreTestFaceCheck(videoElem, statusText, nextBtn);
      } catch (err) {
        console.error("Camera access error:", err);
        statusText.innerHTML = `<i class="bi bi-circle-fill text-danger me-1"></i> Camera Error: ${err.message || 'Permission Denied'}`;
        statusText.classList.remove("bg-dark", "bg-success");
        statusText.classList.add("bg-danger");
        enableBtn.disabled = false;
        nextBtn.disabled = true;
      }
    });
  },

  startPreTestFaceCheck(videoElem, statusText, nextBtn) {
    if (this.preTestFaceCheckInterval) {
      clearInterval(this.preTestFaceCheckInterval);
    }

    this.preTestFaceCheckInterval = setInterval(() => {
      if (!this.hasActiveCamera()) {
        this.handleCameraLoss();
        return;
      }

      if (typeof FaceDetector === "undefined") {
        this.facePresenceVerified = true;
        nextBtn.disabled = false;
        return;
      }

      const analysis = FaceDetector.analyzeFrame(videoElem);

      if (analysis.status === "ok") {
        this.facePresenceVerified = true;
        statusText.innerHTML = '<i class="bi bi-circle-fill text-light me-1"></i> Camera Ready • Face Verified (1 Candidate)';
        statusText.className = "camera-status-overlay bg-success";
        nextBtn.disabled = false;
      } else if (analysis.status === "no_face") {
        this.facePresenceVerified = false;
        statusText.innerHTML = '<i class="bi bi-circle-fill text-dark me-1"></i> No Face Detected • Please sit directly in front of camera';
        statusText.className = "camera-status-overlay bg-warning text-dark";
        nextBtn.disabled = true;
      } else if (analysis.status === "multiple_faces") {
        this.facePresenceVerified = false;
        statusText.innerHTML = '<i class="bi bi-circle-fill text-light me-1"></i> Multiple Faces Detected • Only candidate allowed';
        statusText.className = "camera-status-overlay bg-danger";
        nextBtn.disabled = true;
      } else if (analysis.status === "poor_lighting") {
        this.facePresenceVerified = false;
        statusText.innerHTML = `<i class="bi bi-circle-fill text-dark me-1"></i> ${analysis.message}`;
        statusText.className = "camera-status-overlay bg-warning text-dark";
        nextBtn.disabled = true;
      } else {
        this.facePresenceVerified = false;
        statusText.innerHTML = `<i class="bi bi-circle-fill text-light me-1"></i> ${analysis.message}`;
        statusText.className = "camera-status-overlay bg-dark";
        nextBtn.disabled = true;
      }
    }, 450);
  },

  handleCameraLoss() {
    if (this.preTestFaceCheckInterval) {
      clearInterval(this.preTestFaceCheckInterval);
      this.preTestFaceCheckInterval = null;
    }
    this.facePresenceVerified = false;
    const wasTakingTest = this.currentStep === 4;

    if (this.cameraStream) {
      this.cameraStream.getTracks().forEach(track => track.stop());
      this.cameraStream = null;
    }

    const videoElem = document.getElementById("cameraVideoFeed");
    const fallback = document.getElementById("cameraFallbackPlaceholder");
    const statusText = document.getElementById("cameraStatusText");
    const nextBtn = document.getElementById("btnStep3Next");
    const enableBtn = document.getElementById("btnEnableCamera");

    if (videoElem) {
      videoElem.srcObject = null;
      videoElem.style.display = "none";
    }
    if (fallback) {
      fallback.innerHTML = `
        <div class="text-center p-3">
          <i class="bi bi-camera-video-off fs-1 text-danger mb-2"></i>
          <div class="fw-semibold">Camera Disconnected</div>
          <div class="small text-muted">Reconnect the camera to continue.</div>
        </div>
      `;
      fallback.style.display = "block";
    }
    if (statusText) {
      statusText.innerHTML = '<i class="bi bi-circle-fill text-light me-1"></i> Camera Disconnected';
      statusText.classList.remove("bg-dark", "bg-success");
      statusText.classList.add("bg-danger");
    }
    if (nextBtn) nextBtn.disabled = true;
    if (enableBtn) enableBtn.disabled = false;

    if (wasTakingTest) {
      if (typeof ExamSecurityManager !== "undefined" && ExamSecurityManager.isActive) {
        ExamSecurityManager.recordViolation("camera_disconnect", SecurityConfig.messages.camera_disconnect);
      }
    }
  },

    goToStep(stepNumber) {
    if (stepNumber === 4 && (!this.hasActiveCamera() || !this.facePresenceVerified)) {
      stepNumber = 3;
      App.showToast("An active camera and verified face are required to continue.", "error");
    }

    this.currentStep = stepNumber;

    // Strictly hide all step containers using !important
    document.querySelectorAll(".test-step-view").forEach(v => {
      v.style.setProperty("display", "none", "important");
    });

    const activeEl = document.getElementById(`testStep${stepNumber}`);
    if (activeEl) {
      activeEl.style.setProperty("display", stepNumber === 4 ? "flex" : "block", "important");
    }

    if (stepNumber === 4) {
      document.body.classList.add("assessment-active");
    } else {
      document.body.classList.remove("assessment-active");
    }

    // Scroll smoothly to top on step transitions
    window.scrollTo({ top: 0, behavior: "smooth" });

    // Progress bar update
    const pct = (stepNumber / 4) * 100;
    const bar = document.getElementById("testFlowProgressBar");
    if (bar) bar.style.width = `${pct}%`;
  },

  async startActualTest() {
    if (!this.hasActiveCamera() || !this.facePresenceVerified) {
      this.goToStep(3);
      App.showToast("An active camera and verified face are required to launch the test.", "error");
      return;
    }

    // Stop pre-test face checking loop
    if (this.preTestFaceCheckInterval) {
      clearInterval(this.preTestFaceCheckInterval);
      this.preTestFaceCheckInterval = null;
    }

    const reqCount = this.selectedLength === "max" ? 9999 : (parseInt(this.selectedLength, 10) || 50);
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
    this.initialTimerSeconds = this.timerSeconds;

    this.goToStep(4);
    this.initTimer();
    this.renderQuestionPalette();
    this.renderCurrentQuestion();
    this.bindTestControls();

    // Launch Fullscreen & Anti-Cheating Monitoring
    if (typeof ExamSecurityManager !== "undefined") {
      await ExamSecurityManager.startMonitoring({
        attemptId: this.currentAttemptId,
        testId: this.selectedSubject?.id || 1,
        stream: this.cameraStream,
        videoElem: document.getElementById("cameraVideoFeed")
      });
    }
  },

  shuffleQuestions(questions) {
    const shuffled = [...questions];
    for (let index = shuffled.length - 1; index > 0; index -= 1) {
      const randomIndex = Math.floor(Math.random() * (index + 1));
      [shuffled[index], shuffled[randomIndex]] = [shuffled[randomIndex], shuffled[index]];
    }
    return shuffled;
  },

  initTimer() {
    const timerDisplay = document.getElementById("testLiveTimer");
    if (!timerDisplay) return;
    if (this.timerInterval) clearInterval(this.timerInterval);

    this.timerInterval = setInterval(() => {
      this.timerSeconds--;

      const mins = Math.floor(this.timerSeconds / 60);
      const secs = this.timerSeconds % 60;
      const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      timerDisplay.textContent = formatted;

      const timerContainer = timerDisplay.parentElement;
      if (this.timerSeconds <= 300) {
        timerContainer.classList.add("danger");
      }

      if (this.timerSeconds <= 0) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
        App.showToast("Time expired! Submitting your test automatically.", "warning");
        this.submitFinalTest("Time Expired");
      }
    }, 1000);
  },

  bindTestControls() {
    if (this.testControlsBound) return;
    this.testControlsBound = true;

    document.getElementById("btnPrevQuestion")?.addEventListener("click", () => {
      this.goToPrevQuestion();
    });

    document.getElementById("btnNextQuestion")?.addEventListener("click", () => {
      this.goToNextQuestion();
    });

    document.getElementById("btnMarkReview")?.addEventListener("click", () => {
      const q = this.questions[this.currentIndex];
      if (!q) return;
      if (this.markedForReview.has(q.id)) {
        this.markedForReview.delete(q.id);
        App.showToast("Unmarked from review.", "info");
      } else {
        this.markedForReview.add(q.id);
        App.showToast("Marked for review.", "info");
      }
      this.renderQuestionPalette();
      this.updateNavigationUI();
    });

    document.getElementById("btnClearAnswer")?.addEventListener("click", () => {
      const q = this.questions[this.currentIndex];
      if (!q) return;
      delete this.userAnswers[q.id];
      this.renderCurrentQuestion();
      this.renderQuestionPalette();
      App.showToast("Answer selection cleared.", "info");
    });

    document.getElementById("btnConfirmSubmitTest")?.addEventListener("click", () => {
      const modalEl = document.getElementById("submitConfirmationModal");
      const modal = bootstrap.Modal.getInstance(modalEl);
      if (modal) modal.hide();
      this.submitFinalTest("Candidate Manual Submission");
    });
  },

  selectOption(qId, optIdx) {
    this.userAnswers[qId] = optIdx;

    const optsContainer = document.getElementById("testOptionsContainer");
    if (optsContainer) {
      optsContainer.querySelectorAll(".option-item").forEach(i => {
        const currentIdx = parseInt(i.getAttribute("data-opt-idx"), 10);
        const isSelected = currentIdx === optIdx;
        i.classList.toggle("selected", isSelected);
        i.setAttribute("aria-checked", isSelected ? "true" : "false");

        const indicator = i.querySelector(".option-selection-indicator i");
        if (indicator) {
          indicator.className = `bi ${isSelected ? 'bi-check-circle-fill text-primary' : 'bi-circle text-muted opacity-50'}`;
        }
      });
    }

    this.renderQuestionPalette();
    this.updateNavigationUI();
  },

  updateNavigationUI() {
    const q = this.questions[this.currentIndex];
    const isAnswered = q && this.userAnswers[q.id] !== undefined;
    const selectedIdx = q ? this.userAnswers[q.id] : undefined;
    const optLetter = selectedIdx !== undefined ? (["A", "B", "C", "D"][selectedIdx] || String.fromCharCode(65 + selectedIdx)) : null;
    const isLast = this.currentIndex === this.questions.length - 1;

    // Prev Button
    const prevBtn = document.getElementById("btnPrevQuestion");
    if (prevBtn) {
      prevBtn.disabled = this.currentIndex === 0;
    }

    // Continue / Next Button
    const nextBtn = document.getElementById("btnNextQuestion");
    const continueLabel = document.getElementById("btnContinueLabel");
    const continueIcon = document.getElementById("btnContinueIcon");

    if (nextBtn) {
      if (isLast) {
        if (continueLabel) continueLabel.textContent = "Finish & Submit Test";
        if (continueIcon) continueIcon.className = "bi bi-check2-circle ms-2";
        nextBtn.className = "btn btn-primary-custom px-4 btn-continue btn-finish-test";
      } else {
        if (continueLabel) continueLabel.textContent = "Continue";
        if (continueIcon) continueIcon.className = "bi bi-arrow-right ms-2";
        nextBtn.className = `btn btn-primary-custom px-4 btn-continue ${isAnswered ? 'btn-ready-highlight' : ''}`;
      }
    }

    // Sticky status badge
    const stickyText = document.getElementById("testStickyStatusText");
    const stickyBadge = document.getElementById("testStickyStatusBadge");
    if (stickyText && stickyBadge) {
      if (isAnswered) {
        stickyText.innerHTML = `Option <strong>${optLetter}</strong> selected • Press Continue to proceed`;
        stickyBadge.className = "badge bg-success-subtle text-success border border-success-subtle px-3 py-1";
      } else {
        stickyText.textContent = `Question ${this.currentIndex + 1} of ${this.questions.length} • Select an option to proceed`;
        stickyBadge.className = "badge bg-purple-subtle text-primary border border-primary-subtle px-3 py-1";
      }
    }
  },

  goToNextQuestion() {
    if (this.currentIndex < this.questions.length - 1) {
      this.currentIndex++;
      this.renderCurrentQuestion();
      this.renderQuestionPalette();

      // Reset scroll position of question scroll body so student starts next question at top
      const scrollBody = document.getElementById("testQuestionScrollBody");
      if (scrollBody) {
        scrollBody.scrollTop = 0;
      }
    } else {
      this.showSubmitConfirmationModal();
    }
  },

  goToPrevQuestion() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderCurrentQuestion();
      this.renderQuestionPalette();

      const scrollBody = document.getElementById("testQuestionScrollBody");
      if (scrollBody) {
        scrollBody.scrollTop = 0;
      }
    }
  },

  renderCurrentQuestion() {
    if (!this.questions.length) return;
    const q = this.questions[this.currentIndex];

    // Header info update
    const subLabel = document.getElementById("testCurrentSubjectLabel");
    const diffLabel = document.getElementById("testCurrentDifficultyLabel");
    const counterText = document.getElementById("testQuestionCounterText");
    const qBadge = document.getElementById("testQuestionBadge");

    if (subLabel) subLabel.textContent = this.testSubjectLabel;
    if (diffLabel) diffLabel.textContent = this.testDifficultyLabel;
    if (counterText) counterText.textContent = `Question ${this.currentIndex + 1} of ${this.questions.length}`;
    if (qBadge) qBadge.textContent = `Question ${this.currentIndex + 1} of ${this.questions.length}`;

    // Question body
    const qText = document.getElementById("testQuestionText");
    if (qText) {
      qText.innerHTML = `<span class="text-primary me-2 fw-extrabold">Q${this.currentIndex + 1}.</span> ${q.question_text || q.question}`;
    }

    // Render Options
    const optsContainer = document.getElementById("testOptionsContainer");
    if (!optsContainer) return;

    const selectedOpt = this.userAnswers[q.id];
    let optsHtml = "";

    const rawOptions = q.options || [q.option_a, q.option_b, q.option_c, q.option_d];

    rawOptions.forEach((optText, idx) => {
      const isSelected = selectedOpt === idx;
      const optLetter = ["A", "B", "C", "D"][idx] || String.fromCharCode(65 + idx);

      optsHtml += `
        <div class="option-item ${isSelected ? 'selected' : ''}" 
             data-opt-idx="${idx}" 
             role="radio" 
             aria-checked="${isSelected ? 'true' : 'false'}" 
             tabindex="0"
             id="mockOptItem_${idx}">
          <div class="option-radio-circle">
            <span class="option-radio-dot"></span>
          </div>
          <div class="option-marker">${optLetter}</div>
          <div class="option-text">${optText}</div>
          <div class="option-selection-indicator ms-auto">
            <i class="bi ${isSelected ? 'bi-check-circle-fill text-primary fs-5' : 'bi-circle text-muted opacity-50'}"></i>
          </div>
        </div>
      `;
    });

    optsContainer.innerHTML = optsHtml;

    // Attach click and keyboard handlers to full option cards
    optsContainer.querySelectorAll(".option-item").forEach(item => {
      const handleSelect = () => {
        const idx = parseInt(item.getAttribute("data-opt-idx"), 10);
        this.selectOption(q.id, idx);
      };

      item.addEventListener("click", handleSelect);

      item.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          handleSelect();
        }
      });
    });

    this.updateNavigationUI();
  },

  renderQuestionPalette() {
    const palette = document.getElementById("questionPaletteGrid");
    if (!palette) return;

    let html = "";
    this.questions.forEach((q, idx) => {
      let statusClass = "";
      if (this.markedForReview.has(q.id)) {
        statusClass = "marked";
      } else if (this.userAnswers[q.id] !== undefined) {
        statusClass = "answered";
      }

      if (idx === this.currentIndex) {
        statusClass += " current";
      }

      html += `<div class="palette-item ${statusClass}" data-q-idx="${idx}">${idx + 1}</div>`;
    });

    palette.innerHTML = html;

    palette.querySelectorAll(".palette-item").forEach(item => {
      item.addEventListener("click", () => {
        this.currentIndex = parseInt(item.getAttribute("data-q-idx"), 10);
        this.renderCurrentQuestion();
        this.renderQuestionPalette();
      });
    });
  },

  showSubmitConfirmationModal() {
    let answered = 0;
    this.questions.forEach(q => {
      if (this.userAnswers[q.id] !== undefined) answered++;
    });
    const unanswered = this.questions.length - answered;
    const marked = this.markedForReview.size;

    document.getElementById("modalSubmitAnsweredCount").textContent = answered;
    document.getElementById("modalSubmitUnansweredCount").textContent = unanswered;
    document.getElementById("modalSubmitMarkedCount").textContent = marked;

    const modal = new bootstrap.Modal(document.getElementById("submitConfirmationModal"));
    modal.show();
  },

  async submitFinalTest(submissionReason = "Candidate Manual Submission") {
    if (this.isSubmitting) return;
    this.isSubmitting = true;

    // Disable all submit and continue buttons immediately with clear loading states
    const confirmBtn = document.getElementById("btnConfirmSubmitTest");
    if (confirmBtn) {
      confirmBtn.disabled = true;
      confirmBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Submitting Test...';
    }
    const nextBtn = document.getElementById("btnNextQuestion");
    if (nextBtn) {
      nextBtn.disabled = true;
      nextBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Submitting...';
    }
    const paletteSubmitBtn = document.getElementById("btnSubmitFromPalette");
    if (paletteSubmitBtn) {
      paletteSubmitBtn.disabled = true;
    }

    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }

    // Stop security monitoring & camera stream cleanly
    if (typeof ExamSecurityManager !== "undefined") {
      ExamSecurityManager.stopMonitoring();
    } else if (this.cameraStream) {
      this.cameraStream.getTracks().forEach(t => t.stop());
      this.cameraStream = null;
    }

    const user = API.getCurrentUser();
    if (!user) {
      window.location.replace(API.getLoginUrl());
      return;
    }
    let correct = 0;
    let incorrect = 0;
    let skipped = 0;

    const detailedReview = [];

    const storeQuestions = (API._getQuestionsStore && API._getQuestionsStore()) || [];
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
    });

    const total = this.questions.length;
    const scorePct = total > 0 ? Math.round((correct / total) * 100) : 0;
    const timeSpentMinutes = Math.max(1, Math.ceil(((this.initialTimerSeconds || 900) - this.timerSeconds) / 60));

    const violationsCount = typeof ExamSecurityManager !== "undefined" ? ExamSecurityManager.totalViolations : 0;
    const securityEvents = typeof ExamSecurityManager !== "undefined" ? ExamSecurityManager.eventsLog : [];

    const payload = {
      userId: user.id,
      attempt_id: this.currentAttemptId,
      submission_reason: submissionReason,
      violations_count: violationsCount,
      security_events: securityEvents,
      subjectId: this.selectedSubject ? this.selectedSubject.id : "sub_java",
      subjectName: this.selectedSubject ? this.selectedSubject.name : "General Computer Science",
      difficulty: this.testDifficultyLabel,
      totalQuestions: total,
      correct,
      incorrect,
      skipped,
      scorePct,
      timeSpentMinutes,
      detailedReview
    };

    // Synchronize submission with Backend API
    try {
      const token = localStorage.getItem("smt_auth_token") || "";
      const testId = this.selectedSubject ? this.selectedSubject.id : 1;
      const backendAnswers = this.questions.map(q => ({
        question_id: q.id,
        selected_option: this.userAnswers[q.id] !== undefined ? ["A", "B", "C", "D"][this.userAnswers[q.id]] : "NONE"
      }));

      await fetch(`${API.backendBaseUrl}/api/tests/${testId}/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          attempt_id: this.currentAttemptId,
          submission_reason: submissionReason,
          violations_count: violationsCount,
          answers: backendAnswers,
          time_taken: ((this.initialTimerSeconds || 900) - this.timerSeconds)
        })
      });
    } catch (err) {
      console.warn("[MockTestEngine] Backend submit failed or offline; result saved locally:", err);
    }

    // Save to local storage for instant dashboard/results rendering
    await API.submitTestResult(payload);
    window.location.href = "result.html";
  }
};
