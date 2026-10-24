/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Comprehensive Interactive Mock Test Flow Engine
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("mockTestAppView")) {
    MockTestEngine.init();
  }
});

const MockTestEngine = {
  currentStep: 1, // 1: Subject, 2: Difficulty, 3: Camera, 4: Test
  selectedSubject: null,
  testSubjectLabel: "",
  selectedDifficulty: "Medium",
  testDifficultyLabel: "Medium",
  cameraStream: null,
  testControlsBound: false,
  
  // Test State
  questions: [],
  currentIndex: 0,
  userAnswers: {}, // { qId: optionIndex }
  markedForReview: new Set(),
  timerSeconds: 3600, // 60 minutes
  timerInterval: null,

  async init() {
    this.bindStepNavigation();
    await this.renderSubjects();
    this.bindDifficulty();
    this.bindCameraControls();
  },

  async renderSubjects() {
    const subjects = await API.getSubjects();
    const container = document.getElementById("subjectGridContainer");
    if (!container) return;

    let html = "";
    subjects.forEach(sub => {
      html += `
        <div class="subject-card" data-sub-id="${sub.id}" data-sub-name="${sub.name}">
          <div>
            <div class="d-flex align-items-center gap-3 mb-3">
              <div class="stat-icon-wrapper stat-icon-purple">
                <i class="bi ${sub.icon}"></i>
              </div>
              <div>
                <h6 class="fw-bold mb-0">${sub.name}</h6>
                <span class="badge badge-secondary">${sub.category}</span>
              </div>
            </div>
            <p class="text-muted small mb-0">Comprehensive module covering fundamentals, problem solving and conceptual MCQs.</p>
          </div>
          <div class="d-flex justify-content-between align-items-center mt-3 pt-3 border-top">
            <span class="small text-muted"><i class="bi bi-question-circle me-1"></i>50 Questions per test</span>
            <span class="text-primary fw-semibold small">Select Subject <i class="bi bi-chevron-right"></i></span>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;

    // Card click events
    container.querySelectorAll(".subject-card").forEach(card => {
      card.addEventListener("click", () => {
        container.querySelectorAll(".subject-card").forEach(c => c.classList.remove("selected"));
        card.classList.add("selected");
        this.selectedSubject = {
          id: card.getAttribute("data-sub-id"),
          name: card.getAttribute("data-sub-name")
        };
        document.getElementById("btnStep1Next").disabled = false;
      });
    });
  },

  bindStepNavigation() {
    document.getElementById("btnStep1Next")?.addEventListener("click", () => this.goToStep(2));
    document.getElementById("btnStep2Back")?.addEventListener("click", () => this.goToStep(1));
    document.getElementById("btnStep2Next")?.addEventListener("click", () => this.goToStep(3));
    document.getElementById("btnStep3Back")?.addEventListener("click", () => this.goToStep(2));
    document.getElementById("btnStep3Next")?.addEventListener("click", () => {
      if (!this.hasActiveCamera()) {
        App.showToast("An active camera is required to continue.", "error");
        return;
      }

      this.startActualTest();
    });
  },

  bindDifficulty() {
    const cards = document.querySelectorAll(".difficulty-card");
    cards.forEach(card => {
      card.addEventListener("click", () => {
        cards.forEach(c => c.classList.remove("selected"));
        card.classList.add("selected");
        this.selectedDifficulty = card.getAttribute("data-diff");
      });
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
        statusText.innerHTML = '<i class="bi bi-circle-fill text-light me-1"></i> Camera Ready • Proctoring Active';
        statusText.classList.remove("bg-dark", "bg-danger");
        statusText.classList.add("bg-success");
        nextBtn.disabled = !this.hasActiveCamera();
        videoTrack.addEventListener("ended", () => this.handleCameraLoss(), { once: true });
        videoTrack.addEventListener("mute", () => this.handleCameraLoss(), { once: true });
      } catch (err) {
        if (this.cameraStream) {
          this.cameraStream.getTracks().forEach(track => track.stop());
          this.cameraStream = null;
        }
        videoElem.srcObject = null;
        videoElem.style.display = "none";
        fallback.innerHTML = `
          <div class="text-center p-3">
            <i class="bi bi-camera-video-off fs-1 text-danger mb-2"></i>
            <div class="fw-semibold">Camera Access Required</div>
            <div class="small text-muted">Allow camera permission, then try again.</div>
          </div>
        `;
        fallback.style.display = "block";
        statusText.innerHTML = '<i class="bi bi-circle-fill text-light me-1"></i> Camera Required • Access unavailable';
        statusText.classList.remove("bg-dark", "bg-success");
        statusText.classList.add("bg-danger");
        nextBtn.disabled = true;
        App.showToast("Camera access is required to take this test. Allow access and try again.", "error");
      } finally {
        enableBtn.disabled = false;
      }
    });
  },

  handleCameraLoss() {
    if (!this.cameraStream) return;

    const stream = this.cameraStream;
    const wasTakingTest = this.currentStep === 4;
    this.cameraStream = null;
    stream.getTracks().forEach(track => {
      if (track.readyState === "live") track.stop();
    });

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
      if (this.timerInterval) clearInterval(this.timerInterval);
      this.timerInterval = null;
      this.goToStep(3);
      App.showToast("Camera disconnected. The test is paused until the camera is active again.", "error");
    }
  },

  goToStep(stepNumber) {
    if (stepNumber === 4 && !this.hasActiveCamera()) {
      stepNumber = 3;
      App.showToast("An active camera is required to continue.", "error");
    }

    this.currentStep = stepNumber;
    document.querySelectorAll(".test-step-view").forEach(v => v.style.display = "none");
    document.getElementById(`testStep${stepNumber}`).style.display = "block";

    // Progress bar update
    const pct = (stepNumber / 4) * 100;
    const bar = document.getElementById("testFlowProgressBar");
    if (bar) bar.style.width = `${pct}%`;
  },

  async startActualTest() {
    if (!this.hasActiveCamera()) {
      this.goToStep(3);
      App.showToast("An active camera is required to launch the test.", "error");
      return;
    }

    const requiredQuestionCount = 50;
    this.testSubjectLabel = this.selectedSubject.name;
    this.questions = await API.getQuestions(this.selectedSubject.id, this.selectedDifficulty);
    this.testDifficultyLabel = this.selectedDifficulty;

    if (this.questions.length < requiredQuestionCount) {
      this.questions = await API.getQuestions(this.selectedSubject.id);
      this.testDifficultyLabel = "All Levels";
    }

    if (this.questions.length < requiredQuestionCount) {
      this.questions = await API.getQuestions();
      this.testSubjectLabel = "CSE Comprehensive Assessment";
      this.testDifficultyLabel = "All Subjects";
    }

    if (this.questions.length < requiredQuestionCount) {
      this.questions = [];
      this.goToStep(1);
      App.showToast("The question bank needs at least 50 questions to start this assessment.", "error");
      return;
    }

    this.questions = this.shuffleQuestions(this.questions).slice(0, requiredQuestionCount);

    this.goToStep(4);
    this.initTimer();
    this.renderQuestionPalette();
    this.renderCurrentQuestion();
    this.bindTestControls();
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
      if (this.currentStep === 4 && !this.hasActiveCamera()) {
        this.handleCameraLoss();
        return;
      }

      this.timerSeconds--;

      const mins = Math.floor(this.timerSeconds / 60);
      const secs = this.timerSeconds % 60;
      const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      timerDisplay.textContent = formatted;

      const timerContainer = timerDisplay.parentElement;
      if (this.timerSeconds <= 300 && this.timerSeconds > 60) {
        timerContainer.className = "timer-badge timer-warning";
      } else if (this.timerSeconds <= 60) {
        timerContainer.className = "timer-badge timer-critical";
      }

      if (this.timerSeconds <= 0) {
        clearInterval(this.timerInterval);
        App.showToast("Time expired! Automatically submitting your test...", "warning");
        this.submitTestFinal();
      }
    }, 1000);
  },

  renderCurrentQuestion() {
    const q = this.questions[this.currentIndex];
    if (!q) return;

    document.getElementById("testCurrentSubjectLabel").textContent = this.testSubjectLabel || (this.selectedSubject ? this.selectedSubject.name : "Mock Test");
    document.getElementById("testCurrentDifficultyLabel").textContent = this.testDifficultyLabel;
    document.getElementById("testQuestionCounterText").textContent = `Question ${this.currentIndex + 1} of ${this.questions.length}`;

    const qTextElem = document.getElementById("testQuestionText");
    qTextElem.textContent = q.question;

    const optionsContainer = document.getElementById("testOptionsContainer");
    let optionsHtml = "";

    const prefixes = ["A", "B", "C", "D"];
    q.options.forEach((opt, idx) => {
      const isSelected = this.userAnswers[q.id] === idx;
      optionsHtml += `
        <div class="question-option-item ${isSelected ? 'selected' : ''}" data-opt-idx="${idx}">
          <div class="option-prefix">${prefixes[idx]}</div>
          <div class="flex-grow-1">${opt}</div>
        </div>
      `;
    });

    optionsContainer.innerHTML = optionsHtml;

    // Attach click events
    optionsContainer.querySelectorAll(".question-option-item").forEach(item => {
      item.addEventListener("click", () => {
        const selectedIdx = parseInt(item.getAttribute("data-opt-idx"));
        this.userAnswers[q.id] = selectedIdx;
        this.renderCurrentQuestion();
        this.renderQuestionPalette();
      });
    });

    // Update buttons state
    document.getElementById("btnPrevQuestion").disabled = this.currentIndex === 0;
    const nextBtn = document.getElementById("btnNextQuestion");
    nextBtn.textContent = this.currentIndex === this.questions.length - 1 ? "Review & Submit" : "Next Question";
  },

  renderQuestionPalette() {
    const paletteGrid = document.getElementById("questionPaletteGrid");
    if (!paletteGrid) return;

    let html = "";
    this.questions.forEach((q, idx) => {
      let stateClass = "unanswered";
      if (this.userAnswers[q.id] !== undefined) stateClass = "answered";
      if (this.markedForReview.has(q.id)) stateClass = "marked";
      if (idx === this.currentIndex) stateClass += " current";

      html += `<button type="button" class="palette-btn ${stateClass}" data-q-idx="${idx}">${idx + 1}</button>`;
    });

    paletteGrid.innerHTML = html;

    paletteGrid.querySelectorAll(".palette-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        this.currentIndex = parseInt(btn.getAttribute("data-q-idx"));
        this.renderCurrentQuestion();
        this.renderQuestionPalette();
      });
    });
  },

  bindTestControls() {
    if (this.testControlsBound) return;
    this.testControlsBound = true;

    document.getElementById("btnPrevQuestion")?.addEventListener("click", () => {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.renderCurrentQuestion();
        this.renderQuestionPalette();
      }
    });

    document.getElementById("btnNextQuestion")?.addEventListener("click", () => {
      if (this.currentIndex < this.questions.length - 1) {
        this.currentIndex++;
        this.renderCurrentQuestion();
        this.renderQuestionPalette();
      } else {
        this.showSubmitConfirmationModal();
      }
    });

    document.getElementById("btnMarkReview")?.addEventListener("click", () => {
      const q = this.questions[this.currentIndex];
      if (this.markedForReview.has(q.id)) {
        this.markedForReview.delete(q.id);
      } else {
        this.markedForReview.add(q.id);
      }
      this.renderQuestionPalette();
    });

    document.getElementById("btnClearAnswer")?.addEventListener("click", () => {
      const q = this.questions[this.currentIndex];
      delete this.userAnswers[q.id];
      this.renderCurrentQuestion();
      this.renderQuestionPalette();
    });

    document.getElementById("btnConfirmSubmitTest")?.addEventListener("click", () => {
      this.submitTestFinal();
    });
  },

  showSubmitConfirmationModal() {
    const answeredCount = Object.keys(this.userAnswers).length;
    const totalCount = this.questions.length;
    const unansweredCount = totalCount - answeredCount;

    document.getElementById("modalSubmitAnsweredCount").textContent = answeredCount;
    document.getElementById("modalSubmitUnansweredCount").textContent = unansweredCount;
    document.getElementById("modalSubmitMarkedCount").textContent = this.markedForReview.size;

    const modal = new bootstrap.Modal(document.getElementById("submitConfirmationModal"));
    modal.show();
  },

  async submitTestFinal() {
    if (!this.hasActiveCamera()) {
      this.handleCameraLoss();
      this.goToStep(3);
      App.showToast("An active camera is required to submit this test.", "error");
      return;
    }

    if (this.timerInterval) clearInterval(this.timerInterval);
    if (this.cameraStream) {
      this.cameraStream.getTracks().forEach(track => track.stop());
      this.cameraStream = null;
    }

    const user = API.getCurrentUser() || { id: "usr_student_01" };
    let correct = 0;
    let incorrect = 0;
    let skipped = 0;

    const detailedReview = [];

    this.questions.forEach(q => {
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
    });

    const total = this.questions.length;
    const scorePct = total > 0 ? Math.round((correct / total) * 100) : 0;
    const timeSpentMinutes = Math.max(1, Math.ceil((3600 - this.timerSeconds) / 60));

    const payload = {
      userId: user.id,
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

    await API.submitTestResult(payload);
    window.location.href = "result.html";
  }
};
