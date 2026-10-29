/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Real-Time Proctoring & Examination Security Engine
 *
 * Implements:
 * 1. Fullscreen mode enforcement & exit detection
 * 2. Copy, cut, paste, context menu & developer shortcut restrictions
 * 3. Real-time webcam monitoring & face presence detection with grace periods
 * 4. Tab switching & window focus loss detection
 * 5. Centralized violation tracking & automatic safe submission
 * 6. Clean lifecycle management and safe teardown
 */

const ExamSecurityManager = {
  isActive: false,
  attemptId: null,
  testId: null,
  isSubmitting: false,

  // Violation counters
  violations: {
    tab_switch: 0,
    fullscreen_exit: 0,
    face_missing: 0,
    multiple_faces: 0,
    clipboard_attempt: 0,
    camera_disconnect: 0
  },
  totalViolations: 0,
  eventsLog: [],

  // Timers and references
  faceMonitorInterval: null,
  activeGraceCondition: null,
  graceTimer: null,
  graceSecondsRemaining: 0,
  isPageHidden: false,
  boundHandlers: {},
  cameraStream: null,
  videoElement: null,

  /**
   * Start comprehensive proctoring and security lockdown
   */
  async startMonitoring({ attemptId, testId, stream, videoElem }) {
    if (this.isActive) return;
    this.isActive = true;
    this.isSubmitting = false;
    this.attemptId = attemptId || `att_${Date.now()}`;
    this.testId = testId || 1;
    this.cameraStream = stream;
    this.videoElement = videoElem;

    // Reset counters
    this.violations = {
      tab_switch: 0,
      fullscreen_exit: 0,
      face_missing: 0,
      multiple_faces: 0,
      clipboard_attempt: 0,
      camera_disconnect: 0
    };
    this.totalViolations = 0;
    this.eventsLog = [];

    // 1. Enter Fullscreen Mode
    if (SecurityConfig.enforceFullscreen) {
      await this.enterFullscreen();
    }

    // 2. Hide distraction navigation and show examination shell
    document.body.classList.add("exam-fullscreen-mode");

    // 3. Attach restrictions
    this.bindClipboardAndShortcutRestrictions();
    this.bindVisibilityAndFocusDetection();
    this.bindFullscreenDetection();

    // 4. Setup Floating PiP Webcam Monitor
    this.setupFloatingProctorWidget();

    // 5. Start Real-Time Face & Camera Monitoring Loop
    this.startFaceMonitoringLoop();

    // 6. Update on-screen proctoring status badges
    this.updateStatusIndicators();

    console.log("[ExamSecurity] Proctoring active for attempt:", this.attemptId);
  },

  /**
   * Request browser fullscreen mode
   */
  async enterFullscreen() {
    try {
      const docEl = document.documentElement;
      if (docEl.requestFullscreen) {
        await docEl.requestFullscreen();
      } else if (docEl.webkitRequestFullscreen) {
        await docEl.webkitRequestFullscreen();
      } else if (docEl.msRequestFullscreen) {
        await docEl.msRequestFullscreen();
      }
      this.hideFullscreenReturnModal();
    } catch (err) {
      console.warn("[ExamSecurity] Fullscreen request could not be completed automatically:", err);
      // Show user-action modal if browser requires direct click
      if (this.isActive) {
        this.showFullscreenReturnModal();
      }
    }
  },

  /**
   * Check if browser is currently in fullscreen
   */
  isFullscreenActive() {
    return Boolean(
      document.fullscreenElement ||
      document.webkitFullscreenElement ||
      document.mozFullScreenElement ||
      document.msFullscreenElement
    );
  },

  /**
   * Fullscreen Change Listener
   */
  bindFullscreenDetection() {
    this.boundHandlers.onFullscreenChange = () => {
      if (!this.isActive || this.isSubmitting) return;

      if (!this.isFullscreenActive()) {
        this.recordViolation("fullscreen_exit", SecurityConfig.messages.fullscreen_exit);
        this.showFullscreenReturnModal();
      } else {
        this.hideFullscreenReturnModal();
      }
      this.updateStatusIndicators();
    };

    document.addEventListener("fullscreenchange", this.boundHandlers.onFullscreenChange);
    document.addEventListener("webkitfullscreenchange", this.boundHandlers.onFullscreenChange);
  },

  /**
   * Copy, Cut, Paste, Context Menu, and Developer Shortcut restrictions
   */
  bindClipboardAndShortcutRestrictions() {
    // 1. Prevent context menu
    this.boundHandlers.onContextMenu = (e) => {
      if (!this.isActive) return;
      e.preventDefault();
      this.recordViolation("clipboard_attempt", "Right-click context menu is disabled during the test.");
    };
    document.addEventListener("contextmenu", this.boundHandlers.onContextMenu);

    // 2. Prevent Copy
    this.boundHandlers.onCopy = (e) => {
      if (!this.isActive) return;
      e.preventDefault();
      this.recordViolation("clipboard_attempt", "Copying examination content is restricted.");
    };
    document.addEventListener("copy", this.boundHandlers.onCopy);

    // 3. Prevent Cut
    this.boundHandlers.onCut = (e) => {
      if (!this.isActive) return;
      e.preventDefault();
      this.recordViolation("clipboard_attempt", "Cutting examination content is restricted.");
    };
    document.addEventListener("cut", this.boundHandlers.onCut);

    // 4. Prevent Paste
    this.boundHandlers.onPaste = (e) => {
      if (!this.isActive) return;
      e.preventDefault();
      this.recordViolation("clipboard_attempt", "Pasting into the examination interface is restricted.");
    };
    document.addEventListener("paste", this.boundHandlers.onPaste);

    // 5. Detect and block restricted keyboard shortcuts
    this.boundHandlers.onKeyDown = (e) => {
      if (!this.isActive) return;

      const isCtrlOrCmd = e.ctrlKey || e.metaKey;
      const key = e.key ? e.key.toLowerCase() : "";

      // Restricted combos: Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+A, Ctrl+U, Ctrl+S, Ctrl+P
      if (isCtrlOrCmd && ["c", "v", "x", "a", "u", "s", "p"].includes(key)) {
        e.preventDefault();
        e.stopPropagation();
        this.recordViolation("clipboard_attempt", `Shortcut Ctrl+${key.toUpperCase()} is restricted.`);
        return false;
      }

      // F12 or Developer Tools combos: Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C
      if (e.key === "F12" || (isCtrlOrCmd && e.shiftKey && ["i", "j", "c"].includes(key))) {
        e.preventDefault();
        e.stopPropagation();
        this.recordViolation("clipboard_attempt", "Developer Inspection tools are restricted.");
        return false;
      }

      // Prevent F5 / Ctrl+R refresh
      if (e.key === "F5" || (isCtrlOrCmd && key === "r")) {
        e.preventDefault();
        e.stopPropagation();
        App.showToast("Page refresh is disabled during active examination.", "warning");
        return false;
      }
    };
    window.addEventListener("keydown", this.boundHandlers.onKeyDown, true);
  },

  /**
   * Tab switching and window focus detection using Page Visibility API
   */
  bindVisibilityAndFocusDetection() {
    let focusBlurDebounceTimer = null;

    // Visibility API change
    this.boundHandlers.onVisibilityChange = () => {
      if (!this.isActive || this.isSubmitting) return;

      if (document.visibilityState === "hidden") {
        this.isPageHidden = true;
      } else if (document.visibilityState === "visible") {
        if (this.isPageHidden) {
          this.isPageHidden = false;
          this.recordViolation("tab_switch", SecurityConfig.messages.tab_switch);
        }
      }
    };
    document.addEventListener("visibilitychange", this.boundHandlers.onVisibilityChange);

    // Window Blur (minimized or clicked away)
    this.boundHandlers.onWindowBlur = () => {
      if (!this.isActive || this.isSubmitting) return;

      if (focusBlurDebounceTimer) clearTimeout(focusBlurDebounceTimer);
      focusBlurDebounceTimer = setTimeout(() => {
        if (this.isActive && !this.isPageHidden) {
          this.isPageHidden = true;
        }
      }, (SecurityConfig.focusLossGraceSeconds || 1) * 1000);
    };
    window.addEventListener("blur", this.boundHandlers.onWindowBlur);

    // Window Focus (returned)
    this.boundHandlers.onWindowFocus = () => {
      if (!this.isActive || this.isSubmitting) return;

      if (focusBlurDebounceTimer) clearTimeout(focusBlurDebounceTimer);
      if (this.isPageHidden) {
        this.isPageHidden = false;
        this.recordViolation("tab_switch", "Window focus was lost and restored.");
      }
    };
    window.addEventListener("focus", this.boundHandlers.onWindowFocus);
  },

  /**
   * Continuous Face Detection & Camera Monitoring Loop
   */
  startFaceMonitoringLoop() {
    if (this.faceMonitorInterval) clearInterval(this.faceMonitorInterval);

    this.faceMonitorInterval = setInterval(() => {
      if (!this.isActive || this.isSubmitting) return;

      // 1. Verify Camera Stream
      const isCameraLive = Boolean(
        this.cameraStream &&
        this.cameraStream.getVideoTracks().some(t => t.enabled && t.readyState === "live")
      );

      if (!isCameraLive) {
        this.handleCameraCondition("camera_disconnect", SecurityConfig.messages.camera_disconnect, SecurityConfig.cameraDisconnectGraceSeconds || 5);
        return;
      }

      // 2. Vision analysis via FaceDetector
      const analysis = FaceDetector.analyzeFrame(this.videoElement);
      this.updatePiPStatus(analysis);

      if (analysis.status === "ok") {
        // Face is present and verified: Clear active grace timer
        this.clearGraceCondition();
      } else if (analysis.status === "no_face") {
        this.handleCameraCondition("face_missing", SecurityConfig.messages.face_missing, SecurityConfig.faceMissingGraceSeconds || 5);
      } else if (analysis.status === "multiple_faces") {
        this.handleCameraCondition("multiple_faces", SecurityConfig.messages.multiple_faces, SecurityConfig.multipleFacesGraceSeconds || 3);
      } else if (analysis.status === "poor_lighting" || analysis.status === "face_offcenter") {
        this.handleCameraCondition("face_missing", analysis.message, SecurityConfig.faceMissingGraceSeconds || 5);
      }
    }, SecurityConfig.faceDetectionIntervalMs || 600);
  },

  /**
   * Manage grace period countdown before recording a confirmed violation
   */
  handleCameraCondition(conditionType, message, graceSeconds) {
    if (this.isSubmitting) return;

    if (this.activeGraceCondition === conditionType) {
      // Grace period is already ticking
      return;
    }

    // Start new grace period
    this.activeGraceCondition = conditionType;
    this.graceSecondsRemaining = graceSeconds;
    this.showGraceNotice(message, this.graceSecondsRemaining);

    if (this.graceTimer) clearInterval(this.graceTimer);

    this.graceTimer = setInterval(() => {
      this.graceSecondsRemaining--;

      if (this.graceSecondsRemaining > 0) {
        this.showGraceNotice(message, this.graceSecondsRemaining);
      } else {
        // Grace period expired and condition persists: Record violation
        clearInterval(this.graceTimer);
        this.graceTimer = null;
        this.activeGraceCondition = null;
        this.hideGraceNotice();

        this.recordViolation(conditionType, message);
      }
    }, 1000);
  },

  /**
   * Clear active grace period when student returns to normal state
   */
  clearGraceCondition() {
    if (this.activeGraceCondition) {
      this.activeGraceCondition = null;
      if (this.graceTimer) {
        clearInterval(this.graceTimer);
        this.graceTimer = null;
      }
      this.hideGraceNotice();
    }
  },

  /**
   * Record a security violation, log it to backend, and check auto-submission threshold
   */
  async recordViolation(eventType, message) {
    if (!this.isActive || this.isSubmitting) return;

    const count = (this.violations[eventType] || 0) + 1;
    this.violations[eventType] = count;
    this.totalViolations++;

    const timestamp = new Date().toISOString();
    const eventObj = {
      attempt_id: this.attemptId,
      event_type: eventType,
      message,
      violation_count: count,
      timestamp
    };
    this.eventsLog.push(eventObj);

    console.warn(`[ExamSecurity Violation] ${eventType} (#${count}): ${message}`);

    // Update on-screen warning banner
    this.showSecurityWarningBanner(eventType, message, count);
    this.updateStatusIndicators();

    // Send security event to backend
    this.syncSecurityEventWithBackend(eventObj);

    // Determine configured limit for this event type
    let maxAllowed = 3;
    if (eventType === "fullscreen_exit") maxAllowed = SecurityConfig.maxFullscreenExitViolations;
    else if (eventType === "tab_switch") maxAllowed = SecurityConfig.maxTabSwitchViolations;
    else if (eventType === "face_missing") maxAllowed = SecurityConfig.maxFaceMissingViolations;
    else if (eventType === "multiple_faces") maxAllowed = SecurityConfig.maxMultipleFacesViolations;
    else if (eventType === "clipboard_attempt") maxAllowed = SecurityConfig.maxClipboardViolations;
    else if (eventType === "camera_disconnect") maxAllowed = SecurityConfig.maxCameraDisconnectViolations;

    // Check if violation limit exceeded
    if (count >= maxAllowed) {
      const reason = `Security Violation Limit Exceeded: ${eventType} (${count}/${maxAllowed})`;
      this.triggerAutoSubmission(reason);
    } else if (this.totalViolations >= SecurityConfig.maxTotalViolations) {
      const reason = `Total Security Violation Limit Exceeded (${this.totalViolations}/${SecurityConfig.maxTotalViolations})`;
      this.triggerAutoSubmission(reason);
    }
  },

  /**
   * Log security event to backend REST API with offline graceful fallback
   */
  async syncSecurityEventWithBackend(eventObj) {
    try {
      const user = API.getCurrentUser() || {};
      const token = localStorage.getItem("smt_auth_token") || "";

      await fetch(`${API.backendBaseUrl}/api/tests/${this.testId}/security-event`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          attempt_id: this.attemptId,
          event_type: eventObj.event_type,
          timestamp: eventObj.timestamp,
          details: {
            message: eventObj.message,
            violation_count: eventObj.violation_count
          }
        })
      });
    } catch (err) {
      // Gracefully persist to localStorage if backend network has glitch
      const localEvents = JSON.parse(localStorage.getItem("smt_security_events") || "[]");
      localEvents.push(eventObj);
      localStorage.setItem("smt_security_events", JSON.stringify(localEvents));
    }
  },

  /**
   * Trigger automatic submission safely with mutex lock
   */
  triggerAutoSubmission(reason) {
    if (this.isSubmitting) return;
    this.isSubmitting = true;

    console.warn("[ExamSecurity] AUTO-SUBMITTING EXAMINATION:", reason);

    // Show termination overlay
    this.showAutoSubmissionOverlay(reason);

    // Call MockTestEngine final submission with security reason
    if (typeof MockTestEngine !== "undefined" && typeof MockTestEngine.submitTestFinal === "function") {
      MockTestEngine.submitTestFinal(reason);
    }
  },

  /**
   * Clean up all event listeners, camera tracks, timers, and fullscreen
   */
  stopMonitoring() {
    this.isActive = false;

    // Clear intervals and timers
    if (this.faceMonitorInterval) {
      clearInterval(this.faceMonitorInterval);
      this.faceMonitorInterval = null;
    }
    if (this.graceTimer) {
      clearInterval(this.graceTimer);
      this.graceTimer = null;
    }

    // Remove event listeners
    if (this.boundHandlers.onFullscreenChange) {
      document.removeEventListener("fullscreenchange", this.boundHandlers.onFullscreenChange);
      document.removeEventListener("webkitfullscreenchange", this.boundHandlers.onFullscreenChange);
    }
    if (this.boundHandlers.onContextMenu) {
      document.removeEventListener("contextmenu", this.boundHandlers.onContextMenu);
    }
    if (this.boundHandlers.onCopy) {
      document.removeEventListener("copy", this.boundHandlers.onCopy);
    }
    if (this.boundHandlers.onCut) {
      document.removeEventListener("cut", this.boundHandlers.onCut);
    }
    if (this.boundHandlers.onPaste) {
      document.removeEventListener("paste", this.boundHandlers.onPaste);
    }
    if (this.boundHandlers.onKeyDown) {
      window.removeEventListener("keydown", this.boundHandlers.onKeyDown, true);
    }
    if (this.boundHandlers.onVisibilityChange) {
      document.removeEventListener("visibilitychange", this.boundHandlers.onVisibilityChange);
    }
    if (this.boundHandlers.onWindowBlur) {
      window.removeEventListener("blur", this.boundHandlers.onWindowBlur);
    }
    if (this.boundHandlers.onWindowFocus) {
      window.removeEventListener("focus", this.boundHandlers.onWindowFocus);
    }

    // Stop webcam stream tracks
    if (this.cameraStream) {
      this.cameraStream.getTracks().forEach(track => {
        if (track.readyState === "live") track.stop();
      });
      this.cameraStream = null;
    }

    // Exit fullscreen mode safely
    if (this.isFullscreenActive()) {
      try {
        if (document.exitFullscreen) document.exitFullscreen();
        else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
      } catch (e) {}
    }

    // Remove fullscreen examination CSS class
    document.body.classList.remove("exam-fullscreen-mode");

    // Remove PiP widget and warning banners
    this.removeFloatingProctorWidget();
    this.hideSecurityWarningBanner();
    this.hideGraceNotice();
    this.hideFullscreenReturnModal();

    console.log("[ExamSecurity] Monitoring cleanly stopped.");
  },

  // ================= UI COMPONENTS & OVERLAYS =================

  /**
   * Setup floating Picture-in-Picture webcam monitor in corner
   */
  setupFloatingProctorWidget() {
    let widget = document.getElementById("proctorPipWidget");
    if (!widget) {
      widget = document.createElement("div");
      widget.id = "proctorPipWidget";
      widget.className = "proctor-pip-widget";
      widget.innerHTML = `
        <div class="proctor-pip-header">
          <span class="proctor-pip-title"><i class="bi bi-shield-check me-1"></i> Live Proctor</span>
          <span class="proctor-pip-badge bg-success" id="pipFaceStatusBadge">Face Verified</span>
        </div>
        <div class="proctor-pip-video-wrap">
          <video id="proctorPipVideo" autoplay playsinline muted></video>
          <div class="proctor-pip-overlay-grid" id="pipOverlayGrid"></div>
        </div>
        <div class="proctor-pip-footer">
          <span id="pipViolationsCountText"><i class="bi bi-exclamation-triangle me-1"></i> Violations: 0</span>
          <span id="pipFullscreenIndicator" class="text-success"><i class="bi bi-fullscreen"></i> Fullscreen</span>
        </div>
      `;
      document.body.appendChild(widget);
    }

    const pipVideo = document.getElementById("proctorPipVideo");
    if (pipVideo && this.cameraStream) {
      pipVideo.srcObject = this.cameraStream;
    }
  },

  removeFloatingProctorWidget() {
    const widget = document.getElementById("proctorPipWidget");
    if (widget) widget.remove();
  },

  updatePiPStatus(analysis) {
    const badge = document.getElementById("pipFaceStatusBadge");
    if (!badge) return;

    if (analysis.status === "ok") {
      badge.className = "proctor-pip-badge bg-success";
      badge.textContent = "Face Verified";
    } else if (analysis.status === "no_face") {
      badge.className = "proctor-pip-badge bg-danger";
      badge.textContent = "Face Missing";
    } else if (analysis.status === "multiple_faces") {
      badge.className = "proctor-pip-badge bg-danger";
      badge.textContent = "Multiple Faces";
    } else if (analysis.status === "poor_lighting") {
      badge.className = "proctor-pip-badge bg-warning text-dark";
      badge.textContent = "Low Light";
    } else {
      badge.className = "proctor-pip-badge bg-secondary";
      badge.textContent = "Monitoring";
    }

    const violElem = document.getElementById("pipViolationsCountText");
    if (violElem) {
      violElem.innerHTML = `<i class="bi bi-exclamation-triangle me-1"></i> Violations: ${this.totalViolations}`;
    }

    const fsElem = document.getElementById("pipFullscreenIndicator");
    if (fsElem) {
      if (this.isFullscreenActive()) {
        fsElem.className = "text-success";
        fsElem.innerHTML = `<i class="bi bi-fullscreen"></i> Fullscreen`;
      } else {
        fsElem.className = "text-danger";
        fsElem.innerHTML = `<i class="bi bi-fullscreen-exit"></i> Windowed`;
      }
    }
  },

  /**
   * Update header proctoring badges
   */
  updateStatusIndicators() {
    const fsBadge = document.getElementById("examFullscreenBadge");
    if (fsBadge) {
      if (this.isFullscreenActive()) {
        fsBadge.className = "badge bg-success";
        fsBadge.innerHTML = `<i class="bi bi-fullscreen me-1"></i> Fullscreen Active`;
      } else {
        fsBadge.className = "badge bg-danger";
        fsBadge.innerHTML = `<i class="bi bi-fullscreen-exit me-1"></i> Fullscreen Required`;
      }
    }

    const violBadge = document.getElementById("examViolationCounterBadge");
    if (violBadge) {
      const maxAllowed = SecurityConfig.maxTotalViolations || 6;
      violBadge.className = this.totalViolations > 0 ? "badge bg-warning text-dark" : "badge bg-secondary";
      violBadge.innerHTML = `<i class="bi bi-shield-exclamation me-1"></i> Violations: ${this.totalViolations} / ${maxAllowed}`;
    }
  },

  /**
   * Display non-intrusive on-screen security warning banner
   */
  showSecurityWarningBanner(eventType, message, count) {
    let banner = document.getElementById("examSecurityWarningBanner");
    if (!banner) {
      banner = document.createElement("div");
      banner.id = "examSecurityWarningBanner";
      banner.className = "exam-security-warning-banner";
      const target = document.getElementById("testStep4") || document.body;
      target.prepend(banner);
    }

    let maxAllowed = 3;
    if (eventType === "fullscreen_exit") maxAllowed = SecurityConfig.maxFullscreenExitViolations;
    else if (eventType === "tab_switch") maxAllowed = SecurityConfig.maxTabSwitchViolations;
    else if (eventType === "face_missing") maxAllowed = SecurityConfig.maxFaceMissingViolations;
    else if (eventType === "multiple_faces") maxAllowed = SecurityConfig.maxMultipleFacesViolations;
    else if (eventType === "clipboard_attempt") maxAllowed = SecurityConfig.maxClipboardViolations;
    else if (eventType === "camera_disconnect") maxAllowed = SecurityConfig.maxCameraDisconnectViolations;

    const remaining = Math.max(0, maxAllowed - count);

    banner.innerHTML = `
      <div class="d-flex align-items-center justify-content-between p-3 border border-danger rounded bg-danger-subtle text-danger mb-3 shadow-sm">
        <div class="d-flex align-items-center gap-3">
          <i class="bi bi-shield-exclamation fs-3 text-danger"></i>
          <div>
            <div class="fw-bold">Security Violation: ${message}</div>
            <div class="small">Violation <strong>${count}</strong> of <strong>${maxAllowed}</strong> (Remaining: ${remaining}) — Exceeding limit triggers automatic test submission.</div>
          </div>
        </div>
        <button type="button" class="btn btn-sm btn-outline-danger" onclick="document.getElementById('examSecurityWarningBanner')?.classList.add('d-none')">
          <i class="bi bi-check2 me-1"></i> Acknowledge
        </button>
      </div>
    `;
    banner.classList.remove("d-none");
  },

  hideSecurityWarningBanner() {
    const banner = document.getElementById("examSecurityWarningBanner");
    if (banner) banner.remove();
  },

  /**
   * Display live grace period recovery countdown banner
   */
  showGraceNotice(message, secondsRemaining) {
    let notice = document.getElementById("examGraceNotice");
    if (!notice) {
      notice = document.createElement("div");
      notice.id = "examGraceNotice";
      notice.className = "exam-grace-notice";
      const target = document.getElementById("testStep4") || document.body;
      target.prepend(notice);
    }

    notice.innerHTML = `
      <div class="p-2 px-3 border border-warning rounded bg-warning-subtle text-dark mb-2 d-flex align-items-center justify-content-between shadow-sm animate-pulse">
        <div class="d-flex align-items-center gap-2 small">
          <i class="bi bi-clock-history text-warning fs-5"></i>
          <span><strong>Action Required:</strong> ${message}</span>
        </div>
        <span class="badge bg-warning text-dark fw-bold">Grace Period: ${secondsRemaining}s</span>
      </div>
    `;
    notice.style.display = "block";
  },

  hideGraceNotice() {
    const notice = document.getElementById("examGraceNotice");
    if (notice) notice.style.display = "none";
  },

  /**
   * Modal prompting student to return to fullscreen
   */
  showFullscreenReturnModal() {
    let modal = document.getElementById("fullscreenReturnModal");
    if (!modal) {
      modal = document.createElement("div");
      modal.id = "fullscreenReturnModal";
      modal.className = "fullscreen-prompt-backdrop";
      modal.innerHTML = `
        <div class="fullscreen-prompt-card">
          <i class="bi bi-fullscreen-exit text-danger display-3 mb-3"></i>
          <h4 class="fw-bold text-dark">Fullscreen Mode Exited</h4>
          <p class="text-muted small mb-4">
            You have exited browser fullscreen. Examination rules require full-screen view throughout the test session.
            Exiting fullscreen repeatedly will trigger automatic submission.
          </p>
          <button class="btn btn-primary-custom px-4 py-2 fs-6" id="btnReturnToFullscreen">
            <i class="bi bi-fullscreen me-2"></i> Return to Fullscreen
          </button>
        </div>
      `;
      document.body.appendChild(modal);

      document.getElementById("btnReturnToFullscreen")?.addEventListener("click", async () => {
        await this.enterFullscreen();
      });
    }
    modal.style.display = "flex";
  },

  hideFullscreenReturnModal() {
    const modal = document.getElementById("fullscreenReturnModal");
    if (modal) modal.style.display = "none";
  },

  /**
   * Auto-submission termination notice overlay
   */
  showAutoSubmissionOverlay(reason) {
    let overlay = document.getElementById("examAutoSubmitOverlay");
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.id = "examAutoSubmitOverlay";
      overlay.className = "exam-auto-submit-overlay";
      overlay.innerHTML = `
        <div class="exam-auto-submit-card text-center p-5">
          <div class="spinner-border text-danger mb-4" style="width: 3.5rem; height: 3.5rem;" role="status"></div>
          <h3 class="fw-extrabold text-danger mb-2">Examination Auto-Submitted</h3>
          <p class="text-dark fw-semibold mb-3" id="autoSubmitReasonText">${reason}</p>
          <p class="text-muted small mb-0">Your answers have been securely recorded and evaluated. Redirecting to your performance analytics...</p>
        </div>
      `;
      document.body.appendChild(overlay);
    }
    const reasonText = document.getElementById("autoSubmitReasonText");
    if (reasonText) reasonText.textContent = reason;
    overlay.style.display = "flex";
  }
};

