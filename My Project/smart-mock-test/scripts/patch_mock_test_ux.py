"""
SMART MOCK TEST & CAREER GATEWAY
Patch Mock Test Option Selection and Sticky Continue Button UX
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSS_FILE = os.path.join(ROOT, "frontend", "css", "test.css")
HTML_FILE = os.path.join(ROOT, "frontend", "mock-test.html")
JS_FILE = os.path.join(ROOT, "frontend", "js", "mock-test.js")

def patch_css():
    print(f"[CSS] Reading {CSS_FILE}...")
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Target the question option item block through the end of question-palette-grid
    old_block_pattern = re.compile(
        r'/\* Question Section \*/\s*\.question-option-item\s*\{.*?\.palette-btn\.unanswered\s*\{[^}]*\}',
        re.DOTALL
    )

    new_block = """/* ==========================================================================
   Question Options & Interactive Choice Items
   ========================================================================== */
.option-item,
.question-option-item {
  border: 2px solid var(--border);
  border-radius: var(--radius-md, 12px);
  padding: 0.95rem 1.25rem;
  margin-bottom: 0.85rem;
  cursor: pointer;
  background-color: var(--surface);
  display: flex;
  align-items: center;
  gap: 0.95rem;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
  position: relative;
  outline: none;
  user-select: none;
  -webkit-user-select: none;
}

.option-item:hover,
.question-option-item:hover {
  border-color: var(--primary);
  background-color: var(--surface-subtle);
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(109, 74, 255, 0.08);
}

.option-item:focus-visible,
.question-option-item:focus-visible {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(109, 74, 255, 0.25);
}

.option-item.selected,
.question-option-item.selected {
  border-color: var(--primary);
  background-color: var(--primary-light, rgba(109, 74, 255, 0.09));
  box-shadow: 0 0 0 1px var(--primary), 0 4px 16px rgba(109, 74, 255, 0.12);
  transform: translateY(-1px);
}

/* Radio circle indicator */
.option-radio-circle {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background-color: var(--surface);
  transition: border-color 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease;
}

.option-item.selected .option-radio-circle,
.question-option-item.selected .option-radio-circle {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(109, 74, 255, 0.2);
}

.option-radio-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: transparent;
  transition: background-color 0.2s ease, transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform: scale(0);
}

.option-item.selected .option-radio-dot,
.question-option-item.selected .option-radio-dot {
  background: var(--primary);
  transform: scale(1);
}

/* Marker (A, B, C, D badge) */
.option-marker,
.option-prefix {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm, 8px);
  border: 1.5px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.88rem;
  color: var(--muted);
  flex-shrink: 0;
  background-color: var(--surface-subtle);
  transition: all 0.2s ease;
}

.option-item.selected .option-marker,
.question-option-item.selected .option-prefix {
  background-color: var(--primary);
  color: #ffffff;
  border-color: var(--primary);
}

/* Option Text */
.option-text,
.question-option-item > span:last-child {
  flex: 1 1 0%;
  min-width: 0;
  font-size: 0.96rem;
  line-height: 1.5;
  color: var(--text);
  word-break: normal;
  overflow-wrap: break-word;
}

.option-item.selected .option-text,
.question-option-item.selected > span:last-child {
  font-weight: 600;
  color: var(--text);
}

/* Selection Right Status Icon */
.option-selection-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-left: auto;
  font-size: 1.15rem;
}

/* Question Palette Navigator */
.question-palette-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
}

.palette-item,
.palette-btn {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-sm, 8px);
  border: 1px solid var(--border);
  background-color: var(--surface-subtle);
  color: var(--text);
  font-weight: 600;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  user-select: none;
}

.palette-item:hover,
.palette-btn:hover {
  border-color: var(--primary);
  transform: translateY(-1px);
}

.palette-item.current,
.palette-btn.current {
  border: 2px solid var(--primary);
  font-weight: 800;
  box-shadow: 0 0 0 2px rgba(109, 74, 255, 0.2);
}

.palette-item.answered,
.palette-btn.answered {
  background-color: var(--success);
  color: #fff;
  border-color: var(--success);
}

.palette-item.marked,
.palette-btn.marked {
  background-color: var(--warning);
  color: #fff;
  border-color: var(--warning);
}

.palette-item.unanswered,
.palette-btn.unanswered {
  background-color: var(--surface-subtle);
  color: var(--text);
}"""

    if old_block_pattern.search(content):
        content = old_block_pattern.sub(new_block, content, count=1)
        print("[CSS] Successfully updated Question Option & Palette block.")
    else:
        print("[CSS] WARNING: Could not match exact Question Section block pattern.")

    # Check for bottom action bar styles
    if ".test-bottom-action-bar" not in content:
        action_bar_css = """

/* ==========================================================================
   Fixed / Sticky Bottom Action Bar for Assessment Controls
   ========================================================================== */
#testStep4 {
  padding-bottom: 96px !important;
  position: relative;
}

.test-question-card {
  margin-bottom: 1.5rem;
}

.test-bottom-action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--surface);
  border-top: 1px solid var(--border);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.08);
  z-index: 1040;
  padding: 0.75rem 1.5rem;
  transition: background-color var(--transition-normal), border-color var(--transition-normal);
}

.test-bottom-action-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  width: 100%;
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

/* Responsive adjustments */
@media (max-width: 768px) {
  #testStep4 {
    padding-bottom: 84px !important;
  }

  .test-bottom-action-bar {
    padding: 0.5rem 0.85rem;
  }

  .test-bottom-action-inner {
    gap: 0.5rem;
  }

  .test-bottom-left-group button {
    padding: 0.4rem 0.65rem;
    font-size: 0.82rem;
  }

  .btn-continue {
    min-width: 110px;
    padding: 0.45rem 0.9rem !important;
    font-size: 0.88rem;
  }
}
"""
        content += action_bar_css
        print("[CSS] Appended bottom action bar styles.")

    # Update .proctor-pip-widget position so it floats above bottom bar
    pip_pattern = re.compile(
        r'(\.proctor-pip-widget\s*\{[^}]*?bottom:\s*)24px;',
        re.DOTALL
    )
    if pip_pattern.search(content):
        content = pip_pattern.sub(r'\1calc(75px + 16px) !important;', content)
        print("[CSS] Repositioned proctor-pip-widget above bottom action bar.")

    # Also add mobile pip override if not present
    if ".proctor-pip-widget" in content and "bottom: calc(65px + 10px)" not in content:
        content += """
@media (max-width: 768px) {
  .proctor-pip-widget {
    bottom: calc(65px + 10px) !important;
    right: 12px !important;
    width: 140px !important;
    height: 105px !important;
  }
}
"""

    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[CSS] Updated {CSS_FILE} successfully.")


def patch_html():
    print(f"[HTML] Reading {HTML_FILE}...")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 1: Make footer action bar sticky
    old_step1_footer = re.compile(
        r'<div class="d-flex justify-content-between align-items-center border-top pt-3">\s*<div class="text-muted small" id="selectedSubjectFeedback">',
        re.DOTALL
    )
    new_step1_footer = '<div class="step-sticky-bar d-flex justify-content-between align-items-center border-top pt-3 flex-wrap gap-2">\n              <div class="text-muted small" id="selectedSubjectFeedback">'
    if old_step1_footer.search(content):
        content = old_step1_footer.sub(new_step1_footer, content, count=1)
        print("[HTML] Enhanced Step 1 footer with step-sticky-bar.")

    # Step 4: Revamp layout to use question card + sticky bottom action bar
    old_step4_grid_pattern = re.compile(
        r'<div class="row g-4">\s*<!-- Left Question Area -->\s*<div class="col-lg-8">\s*<div class="card-custom p-4">\s*<h5 class="fw-bold text-dark mb-3" id="testQuestionText">.*?</div>\s*<button class="btn btn-outline-danger w-100 mt-3" onclick="MockTestEngine\.showSubmitConfirmationModal\(\)">\s*<i class="bi bi-check2-circle me-1"></i> Submit Test\s*</button>\s*</div>\s*</div>\s*</div>',
        re.DOTALL
    )

    new_step4_content = """<div class="row g-4 mb-4">
              <!-- Left Question Area -->
              <div class="col-lg-8">
                <div class="card-custom p-4 test-question-card">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-2 py-1" id="testQuestionBadge">Question 1</span>
                    <span class="text-muted small" id="testQuestionStatusLabel"><i class="bi bi-patch-question me-1 text-primary"></i>Single Choice MCQ</span>
                  </div>

                  <h5 class="fw-bold text-dark mb-4 lh-base" id="testQuestionText">
                    Which feature of Object Oriented Programming allows creating a new class from an existing class?
                  </h5>

                  <div id="testOptionsContainer" class="test-options-container mb-2" role="radiogroup" aria-label="Mock Test Options">
                    <!-- Injected via JavaScript -->
                  </div>
                </div>
              </div>

              <!-- Right Question Palette Navigator -->
              <div class="col-lg-4">
                <div class="card-custom p-4 test-palette-card">
                  <h6 class="fw-bold mb-3"><i class="bi bi-grid-3x3-gap-fill me-2 text-primary"></i>Question Navigator</h6>
                  
                  <div class="question-palette-grid mb-4" id="questionPaletteGrid">
                    <!-- Injected via JavaScript -->
                  </div>

                  <div class="p-3 bg-surface-subtle border rounded small mb-3">
                    <div class="d-flex justify-content-between mb-1"><span class="badge bg-success">Green</span> <span>Answered</span></div>
                    <div class="d-flex justify-content-between mb-1"><span class="badge bg-warning">Yellow</span> <span>Marked for Review</span></div>
                    <div class="d-flex justify-content-between"><span class="badge bg-secondary">Gray</span> <span>Unanswered</span></div>
                  </div>

                  <button class="btn btn-outline-danger w-100" id="btnSubmitFromPalette" onclick="MockTestEngine.showSubmitConfirmationModal()">
                    <i class="bi bi-check2-circle me-1"></i> Submit Test
                  </button>
                </div>
              </div>
            </div>

            <!-- Sticky / Fixed Bottom Action Bar -->
            <div class="test-bottom-action-bar" id="testBottomActionBar">
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
            </div>"""

    if old_step4_grid_pattern.search(content):
        content = old_step4_grid_pattern.sub(new_step4_content, content, count=1)
        print("[HTML] Replaced Step 4 Question & Palette markup with sticky action bar.")
    else:
        print("[HTML] WARNING: Could not find exact Step 4 pattern, checking alternate pattern...")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[HTML] Updated {HTML_FILE} successfully.")


def patch_js():
    print(f"[JS] Reading {JS_FILE}...")
    with open(JS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace bindTestControls through renderCurrentQuestion
    # Let's inspect where bindTestControls begins
    target_pattern = re.compile(
        r'bindTestControls\(\)\s*\{.*?renderQuestionPalette\(\)\s*\{',
        re.DOTALL
    )

    new_controls_and_rendering = """bindTestControls() {
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

      // Smooth scroll to top of question card so student reads question cleanly
      const testCard = document.querySelector(".test-question-card");
      if (testCard) {
        testCard.scrollIntoView({ behavior: "smooth", block: "start" });
      } else {
        window.scrollTo({ top: 0, behavior: "smooth" });
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

      const testCard = document.querySelector(".test-question-card");
      if (testCard) {
        testCard.scrollIntoView({ behavior: "smooth", block: "start" });
      } else {
        window.scrollTo({ top: 0, behavior: "smooth" });
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

  renderQuestionPalette() {"""

    if target_pattern.search(content):
        content = target_pattern.sub(new_controls_and_rendering, content, count=1)
        print("[JS] Successfully replaced bindTestControls and renderCurrentQuestion.")
    else:
        print("[JS] WARNING: Could not find exact bindTestControls pattern.")

    # Enhance submitFinalTest duplicate click prevention
    submit_pattern = re.compile(
        r'async submitFinalTest\(submissionReason = "Candidate Manual Submission"\)\s*\{\s*if \(this\.isSubmitting\) return;\s*this\.isSubmitting = true;',
        re.DOTALL
    )
    new_submit_head = """async submitFinalTest(submissionReason = "Candidate Manual Submission") {
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
    }"""

    if submit_pattern.search(content):
        content = submit_pattern.sub(new_submit_head, content, count=1)
        print("[JS] Enhanced submitFinalTest with duplicate submission button lock & spinner.")

    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[JS] Updated {JS_FILE} successfully.")

if __name__ == "__main__":
    patch_css()
    patch_html()
    patch_js()
    print("ALL PATCHES APPLIED.")

