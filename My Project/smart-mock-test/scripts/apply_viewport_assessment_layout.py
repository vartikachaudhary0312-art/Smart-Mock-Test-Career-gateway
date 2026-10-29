"""
SMART MOCK TEST & CAREER GATEWAY
Apply Viewport-Fitted Assessment Layout for Step 4
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HTML_FILE = os.path.join(ROOT, "frontend", "mock-test.html")
CSS_FILE = os.path.join(ROOT, "frontend", "css", "test.css")
JS_FILE = os.path.join(ROOT, "frontend", "js", "mock-test.js")

def patch_html():
    print(f"[HTML] Reading {HTML_FILE}...")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Match Step 4 container
    step4_pattern = re.compile(
        r'<!-- STEP 4: LIVE TEST SCREEN -->\s*<div class="test-step-view"[^>]*id="testStep4"[^>]*>.*?</div>\s*<!-- Submit Confirmation Modal -->',
        re.DOTALL
    )

    new_step4_html = """<!-- STEP 4: LIVE TEST SCREEN -->
          <div class="test-step-view assessment-workspace" id="testStep4" style="display: none;">
            
            <!-- Sticky / Fixed Test Control Header -->
            <div class="test-header-bar flex-shrink-0">
              <div class="d-flex align-items-center gap-2 flex-wrap">
                <span class="fw-bold text-dark fs-5" id="testCurrentSubjectLabel">Java Programming</span>
                <span class="badge badge-purple ms-1" id="testCurrentDifficultyLabel">Medium</span>
                <span class="badge bg-success ms-2" id="examFullscreenBadge"><i class="bi bi-fullscreen me-1"></i>Fullscreen Active</span>
                <span class="badge bg-secondary ms-1" id="examViolationCounterBadge"><i class="bi bi-shield-exclamation me-1"></i>Violations: 0 / 6</span>
              </div>
              
              <div class="d-flex align-items-center gap-3">
                <span class="small text-muted d-none d-md-inline" id="testQuestionCounterText">Question 1 of 50</span>
                <div class="timer-badge">
                  <i class="bi bi-clock-history text-primary"></i>
                  <span id="testLiveTimer">60:00</span>
                </div>
              </div>
            </div>

            <!-- Security Warning and Grace Alert Containers -->
            <div id="examGraceNotice" class="exam-grace-notice flex-shrink-0" style="display: none;"></div>
            <div id="examSecurityWarningBanner" class="exam-security-warning-banner flex-shrink-0 d-none"></div>

            <!-- Assessment Workspace Content (Fits Viewport, Question Scrolls Internally If Long) -->
            <div class="assessment-content-area">
              <div class="assessment-content-inner">
                
                <!-- Left: Question & Options Panel -->
                <div class="assessment-question-col">
                  <div class="card-custom test-question-card">
                    <div class="test-question-meta-header flex-shrink-0">
                      <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-2 py-1" id="testQuestionBadge">Question 1</span>
                      <span class="text-muted small" id="testQuestionStatusLabel"><i class="bi bi-patch-question me-1 text-primary"></i>Single Choice MCQ</span>
                    </div>

                    <!-- Scrollable question & options body -->
                    <div class="test-question-scroll-body" id="testQuestionScrollBody">
                      <h5 class="fw-bold text-dark mb-4 lh-base" id="testQuestionText">
                        Which feature of Object Oriented Programming allows creating a new class from an existing class?
                      </h5>

                      <div id="testOptionsContainer" class="test-options-container mb-2" role="radiogroup" aria-label="Mock Test Options">
                        <!-- Injected via JavaScript -->
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Right: Question Palette Navigator -->
                <div class="assessment-palette-col">
                  <div class="card-custom test-palette-card">
                    <div class="test-palette-header flex-shrink-0 mb-3">
                      <h6 class="fw-bold mb-0"><i class="bi bi-grid-3x3-gap-fill me-2 text-primary"></i>Question Navigator</h6>
                    </div>
                    
                    <div class="test-palette-scroll-body">
                      <div class="question-palette-grid mb-3" id="questionPaletteGrid">
                        <!-- Injected via JavaScript -->
                      </div>

                      <div class="p-3 bg-surface-subtle border rounded small mb-3">
                        <div class="d-flex justify-content-between mb-1"><span class="badge bg-success">Green</span> <span>Answered</span></div>
                        <div class="d-flex justify-content-between mb-1"><span class="badge bg-warning">Yellow</span> <span>Marked for Review</span></div>
                        <div class="d-flex justify-content-between"><span class="badge bg-secondary">Gray</span> <span>Unanswered</span></div>
                      </div>
                    </div>

                    <div class="test-palette-footer flex-shrink-0 pt-2 border-top">
                      <button class="btn btn-outline-danger w-100" id="btnSubmitFromPalette" onclick="MockTestEngine.showSubmitConfirmationModal()">
                        <i class="bi bi-check2-circle me-1"></i> Submit Test
                      </button>
                    </div>
                  </div>
                </div>

              </div>
            </div>

            <!-- Persistent Bottom Action Bar (Docked At Bottom, Always 100% Accessible) -->
            <div class="test-bottom-action-bar flex-shrink-0" id="testBottomActionBar">
              <div class="test-bottom-action-inner content-max-width">
                <div class="test-bottom-left-group">
                  <button class="btn btn-outline-custom" id="btnPrevQuestion">
                    <i class="bi bi-chevron-left me-1"></i> <span class="d-none d-sm-inline">Previous</span>
                  </button>
                  <button class="btn btn-outline-custom text-warning" id="btnMarkReview">
                    <i class="bi bi-bookmark me-1"></i> <span class="d-none d-md-inline">Mark for Review</span><span class="d-inline d-md-none">Review</span>
                  </button>
                  <button class="btn btn-outline-custom text-danger" id="btnClearAnswer">
                    <i class="bi bi-x-circle me-1"></i> <span class="d-none d-md-inline">Clear Choice</span><span class="d-inline d-md-none">Clear</span>
                  </button>
                </div>

                <div class="test-bottom-center-info d-none d-lg-flex align-items-center gap-2">
                  <span class="badge bg-purple-subtle text-primary border border-primary-subtle px-3 py-1" id="testStickyStatusBadge">
                    <i class="bi bi-info-circle me-1"></i> <span id="testStickyStatusText">Select an option to proceed</span>
                  </span>
                </div>

                <div class="test-bottom-right-group d-flex align-items-center gap-2">
                  <button class="btn btn-primary-custom px-4 btn-continue" id="btnNextQuestion">
                    <span id="btnContinueLabel">Continue</span> <i class="bi bi-arrow-right ms-2" id="btnContinueIcon"></i>
                  </button>
                </div>
              </div>
            </div>

          </div>

        </div>
      </div>
    </main>
  </div>

  <!-- Submit Confirmation Modal -->"""

    if step4_pattern.search(content):
        content = step4_pattern.sub(new_step4_html, content, count=1)
        print("[HTML] Replaced Step 4 markup with full viewport assessment workspace.")
    else:
        print("[HTML] WARNING: Could not find exact Step 4 pattern.")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[HTML] Updated {HTML_FILE} successfully.")


def patch_css():
    print(f"[CSS] Reading {CSS_FILE}...")
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace bottom action bar and layout rules with true viewport flex layout
    old_action_bar_pattern = re.compile(
        r'/\* ==========================================================================\s*Fixed / Sticky Bottom Action Bar for Assessment Controls\s*========================================================================== \*/.*',
        re.DOTALL
    )

    new_assessment_css = """/* ==========================================================================
   Full Viewport Assessment Workspace (Step 4)
   ========================================================================== */
body.assessment-active {
  overflow: hidden !important;
  height: 100vh !important;
  max-height: 100vh !important;
}

body.assessment-active .app-main {
  height: 100vh !important;
  max-height: 100vh !important;
  overflow: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  margin-left: 0 !important;
  padding: 0 !important;
}

body.assessment-active .app-header,
body.assessment-active #testFlowProgressBar {
  display: none !important;
}

body.assessment-active .page-body {
  padding: 0 !important;
  flex: 1 1 0% !important;
  min-height: 0 !important;
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
}

body.assessment-active .content-max-width {
  width: 100% !important;
  max-width: 100% !important;
  flex: 1 1 0% !important;
  min-height: 0 !important;
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
}

/* Eliminate transform containment during assessment */
body.assessment-active .page-body,
body.assessment-active .test-step-view,
body.assessment-active .card-custom {
  animation: none !important;
  transform: none !important;
}

/* Workspace container */
.test-step-view.assessment-workspace {
  display: flex !important;
  flex-direction: column !important;
  height: 100vh !important;
  max-height: 100vh !important;
  width: 100% !important;
  overflow: hidden !important;
  position: relative !important;
  padding-bottom: 0 !important;
}

/* Header bar */
.assessment-workspace .test-header-bar {
  flex-shrink: 0 !important;
  height: 54px !important;
  padding: 0.5rem 1.5rem !important;
  background-color: var(--surface) !important;
  border-bottom: 1px solid var(--border) !important;
  border-radius: 0 !important;
  margin-bottom: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  z-index: 10 !important;
}

/* Assessment Content Area */
.assessment-content-area {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  overflow: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  background-color: var(--bg) !important;
}

.assessment-content-inner {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  display: flex !important;
  gap: 1.25rem !important;
  padding: 1rem 1.5rem !important;
  width: 100% !important;
  max-width: 1440px !important;
  margin: 0 auto !important;
  overflow: hidden !important;
}

/* Left Question Column */
.assessment-question-col {
  flex: 1 1 70% !important;
  min-width: 0 !important;
  min-height: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  height: 100% !important;
}

.assessment-question-col .test-question-card {
  height: 100% !important;
  max-height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
  overflow: hidden !important;
  padding: 1.25rem 1.5rem !important;
  margin-bottom: 0 !important;
}

.test-question-meta-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
  flex-shrink: 0;
}

/* Scrollable question text and options */
.test-question-scroll-body {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  padding-right: 0.5rem !important;
}

/* Options Container styling */
.test-options-container {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.test-options-container .option-item {
  margin-bottom: 0 !important;
}

/* Right Question Palette Column */
.assessment-palette-col {
  flex: 0 0 30% !important;
  min-width: 280px !important;
  max-width: 360px !important;
  min-height: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  height: 100% !important;
}

.assessment-palette-col .test-palette-card {
  height: 100% !important;
  max-height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
  overflow: hidden !important;
  padding: 1.25rem !important;
  margin-bottom: 0 !important;
}

.test-palette-scroll-body {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  padding-right: 0.25rem !important;
}

/* Persistent Bottom Action Bar */
.assessment-workspace .test-bottom-action-bar {
  flex-shrink: 0 !important;
  position: relative !important;
  height: 64px !important;
  background-color: var(--surface) !important;
  border-top: 1px solid var(--border) !important;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.06) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 0.6rem 1.5rem !important;
  z-index: 1040 !important;
}

.assessment-workspace .test-bottom-action-inner {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  width: 100% !important;
  max-width: 1440px !important;
  margin: 0 auto !important;
}

.test-bottom-left-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.test-bottom-right-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-continue {
  min-width: 140px;
  font-weight: 600;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: var(--shadow-sm);
}

.btn-continue:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(109, 74, 255, 0.25);
}

.btn-ready-highlight {
  animation: continueReadyGlow 2s infinite;
}

@keyframes continueReadyGlow {
  0% { box-shadow: 0 0 0 0 rgba(109, 74, 255, 0.4); }
  70% { box-shadow: 0 0 0 8px rgba(109, 74, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(109, 74, 255, 0); }
}

.btn-finish-test {
  background-color: #10b981 !important;
  border-color: #10b981 !important;
  color: #ffffff !important;
  font-weight: 700;
}

.btn-finish-test:hover {
  background-color: #059669 !important;
  border-color: #059669 !important;
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35);
}

/* Step 1 Sticky Action Bar */
.step-sticky-bar {
  position: sticky;
  bottom: 0;
  background-color: var(--surface);
  border-top: 1px solid var(--border);
  padding: 1rem 0;
  z-index: 100;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.04);
}

/* Proctor PIP Widget: safely placed above bottom action bar */
body.assessment-active .proctor-pip-widget {
  bottom: calc(64px + 16px) !important;
  right: 20px !important;
  z-index: 1050 !important;
}

/* Mobile & Tablet Responsiveness */
@media (max-width: 991.98px) {
  .assessment-content-inner {
    flex-direction: column !important;
    gap: 0.75rem !important;
    padding: 0.75rem !important;
  }

  .assessment-palette-col {
    display: none !important;
  }

  .assessment-question-col {
    flex: 1 1 auto !important;
    height: 100% !important;
  }

  .assessment-workspace .test-bottom-action-bar {
    height: auto !important;
    padding: 0.5rem 0.75rem !important;
  }

  .btn-continue {
    min-width: 110px !important;
  }

  body.assessment-active .proctor-pip-widget {
    bottom: calc(64px + 10px) !important;
    right: 12px !important;
    width: 140px !important;
    height: 105px !important;
  }
}
"""

    if old_action_bar_pattern.search(content):
        content = old_action_bar_pattern.sub(new_assessment_css, content)
        print("[CSS] Replaced bottom action bar styles with full viewport flex layout.")
    else:
        content += "\n" + new_assessment_css
        print("[CSS] Appended full viewport flex layout styles.")

    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[CSS] Updated {CSS_FILE} successfully.")


def patch_js():
    print(f"[JS] Reading {JS_FILE}...")
    with open(JS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update goToStep to toggle body.assessment-active
    go_to_step_pattern = re.compile(
        r'goToStep\(stepNumber\)\s*\{.*?document\.getElementById\(`testStep\$\{stepNumber\}`\)\.style\.display = "block";',
        re.DOTALL
    )

    new_go_to_step = """goToStep(stepNumber) {
    if (stepNumber === 4 && (!this.hasActiveCamera() || !this.facePresenceVerified)) {
      stepNumber = 3;
      App.showToast("An active camera and verified face are required to continue.", "error");
    }

    this.currentStep = stepNumber;
    document.querySelectorAll(".test-step-view").forEach(v => v.style.display = "none");
    document.getElementById(`testStep${stepNumber}`).style.display = "block";

    if (stepNumber === 4) {
      document.body.classList.add("assessment-active");
    } else {
      document.body.classList.remove("assessment-active");
    }"""

    if go_to_step_pattern.search(content):
        content = go_to_step_pattern.sub(new_go_to_step, content, count=1)
        print("[JS] Updated goToStep with body.assessment-active class management.")
    else:
        print("[JS] WARNING: Could not find goToStep pattern.")

    # 2. Update goToNextQuestion & goToPrevQuestion to reset question scroll container
    scroll_reset_pattern = re.compile(
        r'goToNextQuestion\(\)\s*\{.*?if \(this\.currentIndex < this\.questions\.length - 1\)\s*\{.*?\} else \{\s*this\.showSubmitConfirmationModal\(\);\s*\}',
        re.DOTALL
    )

    new_nav_methods = """goToNextQuestion() {
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
  }"""

    if scroll_reset_pattern.search(content):
        content = scroll_reset_pattern.sub(new_nav_methods, content, count=1)
        print("[JS] Updated goToNextQuestion with testQuestionScrollBody reset.")

    # 3. Ensure submitFinalTest cleans up body.assessment-active
    submit_cleanup_pattern = re.compile(
        r'async submitFinalTest\(submissionReason = "Candidate Manual Submission"\)\s*\{',
        re.DOTALL
    )
    if submit_cleanup_pattern.search(content) and "document.body.classList.remove(\"assessment-active\");" not in content:
        content = submit_cleanup_pattern.sub(
            'async submitFinalTest(submissionReason = "Candidate Manual Submission") {\n    document.body.classList.remove("assessment-active");',
            content, count=1
        )
        print("[JS] Added assessment-active cleanup on test submit.")

    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[JS] Updated {JS_FILE} successfully.")

if __name__ == "__main__":
    patch_html()
    patch_css()
    patch_js()
    print("ALL ASSESSMENT WORKSPACE PATCHES APPLIED.")

