"""
SMART MOCK TEST & CAREER GATEWAY
Permanent Mock Test Layout & Navigation Fix
Fixes:
1. Keeps Start Test & Back to Mock Tests near top of Test Details / Configuration screen (Step 2).
2. Prevents Active Assessment Question screen (Step 4) from rendering at bottom of card listing (Step 1).
3. Positions Next / Continue button & test controls directly below the answer options without empty space.
4. Ensures responsive layout on desktop, laptop, tablet, and mobile.
"""

import os
import re

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
HTML_PATH = os.path.join(FRONTEND_DIR, "mock-test.html")
CSS_PATH = os.path.join(FRONTEND_DIR, "css", "test.css")
JS_PATH = os.path.join(FRONTEND_DIR, "js", "mock-test.js")

# ==========================================
# 1. PATCH mock-test.html
# ==========================================
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# A. Step 2 Top Action Bar and Back/Start buttons
step2_target_pattern = r'(<!-- STEP 2: TEST CONFIGURATION -->\s*<div class="test-step-view" id="testStep2" style="display: none;">\s*)(<div class="mb-3">)'
step2_replacement = r'''\1<!-- Step 2 Top Action Header: Start Test & Back buttons accessible near the top -->
            <div class="card-custom p-3 mb-4 bg-surface border">
              <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
                <button class="btn btn-outline-custom" id="btnStep2BackTop" type="button">
                  <i class="bi bi-arrow-left me-2"></i>Back to Mock Tests
                </button>
                <div class="d-flex align-items-center gap-2">
                  <button class="btn btn-primary-custom px-4" id="btnStep2StartTop" type="button">
                    <i class="bi bi-play-circle-fill me-2"></i>Start Test <i class="bi bi-arrow-right ms-2"></i>
                  </button>
                </div>
              </div>
            </div>

            \2'''

if "btnStep2BackTop" not in html:
    html = re.sub(step2_target_pattern, step2_replacement, html, count=1)

# In Selected Subject summary banner, add quick start button if not present
if "btnStep2QuickStart" not in html:
    banner_target = r'(<div class="text-md-end flex-shrink-0">\s*<span class="text-muted small d-block">Available In Bank</span>\s*<span class="fw-bold fs-5 text-primary" id="cfgSubjectAvailableCount">100 Questions</span>\s*</div>)'
    banner_replacement = r'''<div class="d-flex align-items-center gap-3 flex-wrap">
                  \1
                  <button class="btn btn-primary-custom px-4 d-none d-md-inline-flex align-items-center" id="btnStep2QuickStart" type="button">
                    <i class="bi bi-play-circle-fill me-2"></i>Start Test
                  </button>
                </div>'''
    html = re.sub(banner_target, banner_replacement, html, count=1)

# Step 2 bottom buttons labels
html = re.sub(
    r'<button class="btn btn-outline-custom" id="btnStep2Back">.*?Back.*?</button>',
    r'<button class="btn btn-outline-custom" id="btnStep2Back" type="button"><i class="bi bi-arrow-left me-2"></i>Back to Mock Tests</button>',
    html
)
html = re.sub(
    r'<button class="btn btn-primary-custom px-4" id="btnStep2Next">.*?</button>',
    r'<button class="btn btn-primary-custom px-4" id="btnStep2Next" type="button">Start Test <i class="bi bi-arrow-right ms-2"></i></button>',
    html
)

# Step 3 buttons
html = re.sub(
    r'<button class="btn btn-outline-custom" id="btnStep3Back">.*?Back.*?</button>',
    r'<button class="btn btn-outline-custom" id="btnStep3Back" type="button"><i class="bi bi-arrow-left me-2"></i>Back to Test Details</button>',
    html
)

# B. Step 4 Action Bar Relocation: Place directly below options inside question card
# Check if #testBottomActionBar is currently outside .assessment-question-col
if '<div class="test-bottom-action-bar flex-shrink-0" id="testBottomActionBar">' in html:
    # 1. Remove the external bottom action bar
    external_bar_pattern = r'\s*<!-- Persistent Bottom Action Bar \(Docked At Bottom, Always 100% Accessible\) -->\s*<div class="test-bottom-action-bar flex-shrink-0" id="testBottomActionBar">[\s\S]*?</div>\s*</div>\s*</div>\s*(?=</div>\s*</div>\s*</main>)'
    
    # 2. Extract inner content of bottom action bar
    bar_html = '''
                      <!-- Persistent Action Bar: Directly below the answer options -->
                      <div class="test-bottom-action-bar test-question-actions-toolbar" id="testBottomActionBar">
                        <div class="test-bottom-action-inner">
                          <div class="test-bottom-left-group">
                            <button class="btn btn-outline-custom" id="btnPrevQuestion" type="button">
                              <i class="bi bi-chevron-left me-1"></i> <span class="d-none d-sm-inline">Previous</span>
                            </button>
                            <button class="btn btn-outline-custom text-warning" id="btnMarkReview" type="button">
                              <i class="bi bi-bookmark me-1"></i> <span class="d-none d-md-inline">Mark for Review</span><span class="d-inline d-md-none">Review</span>
                            </button>
                            <button class="btn btn-outline-custom text-danger" id="btnClearAnswer" type="button">
                              <i class="bi bi-x-circle me-1"></i> <span class="d-none d-md-inline">Clear Choice</span><span class="d-inline d-md-none">Clear</span>
                            </button>
                          </div>

                          <div class="test-bottom-center-info d-none d-lg-flex align-items-center gap-2">
                            <span class="badge bg-purple-subtle text-primary border border-primary-subtle px-3 py-1" id="testStickyStatusBadge">
                              <i class="bi bi-info-circle me-1"></i> <span id="testStickyStatusText">Select an option to proceed</span>
                            </span>
                          </div>

                          <div class="test-bottom-right-group d-flex align-items-center gap-2">
                            <button class="btn btn-outline-danger d-lg-none" id="btnMobileSubmitTest" type="button" onclick="MockTestEngine.showSubmitConfirmationModal()">
                              <i class="bi bi-check2-circle me-1"></i> Submit
                            </button>
                            <button class="btn btn-primary-custom px-4 btn-continue" id="btnNextQuestion" type="button">
                              <span id="btnContinueLabel">Continue</span> <i class="bi bi-arrow-right ms-2" id="btnContinueIcon"></i>
                            </button>
                          </div>
                        </div>
                      </div>'''

    # Place inside #testQuestionScrollBody directly below #testOptionsContainer
    options_target = r'(<div id="testOptionsContainer" class="test-options-container mb-2" role="radiogroup" aria-label="Mock Test Options">\s*<!-- Injected via JavaScript -->\s*</div>)'
    options_replacement = r'\1\n' + bar_html

    html = re.sub(options_target, options_replacement, html, count=1)
    html = re.sub(external_bar_pattern, '', html, count=1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("[OK] mock-test.html patched.")

# ==========================================
# 2. PATCH test.css
# ==========================================
with open(CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()

# Replace unconditional .test-step-view.assessment-workspace rule
old_ws_rule = """.test-step-view.assessment-workspace {
  display: flex !important;
  flex-direction: column !important;
  height: 100vh !important;
  max-height: 100vh !important;
  width: 100% !important;
  overflow: hidden !important;
  position: relative !important;
  padding-bottom: 0 !important;
}"""

new_ws_rule = """/* By default Step 4 assessment workspace is strictly hidden */
#testStep4.assessment-workspace {
  display: none !important;
}

/* Only when assessment-active class is on body and step 4 is active */
body.assessment-active #testStep4.assessment-workspace {
  display: flex !important;
  flex-direction: column !important;
  height: 100vh !important;
  max-height: 100vh !important;
  width: 100% !important;
  overflow: hidden !important;
  position: relative !important;
  padding-bottom: 0 !important;
}"""

if old_ws_rule in css:
    css = css.replace(old_ws_rule, new_ws_rule)
else:
    # Regex fallback
    css = re.sub(
        r'\.test-step-view\.assessment-workspace\s*\{[^}]*\}',
        new_ws_rule,
        css,
        count=1
    )

# Patch action bar CSS to sit cleanly directly below options
old_bar_css = """.assessment-workspace .test-bottom-action-bar {
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
}"""

new_bar_css = """.test-question-actions-toolbar,
.assessment-workspace .test-bottom-action-bar {
  flex-shrink: 0 !important;
  position: relative !important;
  background-color: var(--surface) !important;
  border-top: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 0.85rem 0.75rem 0.4rem 0.75rem !important;
  margin-top: 1.25rem !important;
  margin-bottom: 0.5rem !important;
  z-index: 10 !important;
  box-shadow: none !important;
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
}"""

if old_bar_css in css:
    css = css.replace(old_bar_css, new_bar_css)
else:
    css = re.sub(
        r'\.assessment-workspace\s+\.test-bottom-action-bar\s*\{[^}]*\}',
        new_bar_css,
        css,
        count=1
    )

with open(CSS_PATH, "w", encoding="utf-8") as f:
    f.write(css)
print("[OK] test.css patched.")

# ==========================================
# 3. PATCH mock-test.js
# ==========================================
with open(JS_PATH, "r", encoding="utf-8") as f:
    js = f.read()

# A. Update goToStep to strictly enforce display: none !important on inactive steps
old_go_to_step = """  goToStep(stepNumber) {
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
    }

    // Progress bar update
    const pct = (stepNumber / 4) * 100;
    const bar = document.getElementById("testFlowProgressBar");
    if (bar) bar.style.width = `${pct}%`;
  },"""

new_go_to_step = """  goToStep(stepNumber) {
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
  },"""

if old_go_to_step in js:
    js = js.replace(old_go_to_step, new_go_to_step)
else:
    js = re.sub(
        r'goToStep\(stepNumber\)\s*\{[\s\S]*?if\s*\(bar\)\s*bar\.style\.width\s*=\s*`\$\{pct\}%`;\s*\},',
        new_go_to_step,
        js,
        count=1
    )

# B. Card click immediately opens Step 2 (Test Details Screen)
old_card_click = """    // Card click events
    container.querySelectorAll(".subject-card").forEach(card => {
      card.addEventListener("click", () => {
        const subId = card.getAttribute("data-sub-id");
        const found = this.allSubjects.find(s => s.id === subId);
        if (found) {
          this.selectSubject(found);
        }
      });
    });"""

new_card_click = """    // Card click events: Selecting a card transitions immediately to Test Details (Step 2)
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
    });"""

if old_card_click in js:
    js = js.replace(old_card_click, new_card_click)
else:
    js = re.sub(
        r'// Card click events[\s\S]*?container\.querySelectorAll\("\.subject-card"\)\.forEach\([\s\S]*?\}\);\s*\}\);',
        new_card_click,
        js,
        count=1
    )

# C. Bind Step 2 top buttons and start buttons
old_bind_nav = """  bindStepNavigation() {
    document.getElementById("btnStep1Next")?.addEventListener("click", () => {
      if (!this.selectedSubject) {
        App.showToast("Please select a subject module first.", "warning");
        return;
      }
      this.goToStep(2);
    });

    document.getElementById("btnStep2Back")?.addEventListener("click", () => this.goToStep(1));
    document.getElementById("btnStep2Next")?.addEventListener("click", () => this.goToStep(3));"""

new_bind_nav = """  bindStepNavigation() {
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
    document.getElementById("btnStep2QuickStart")?.addEventListener("click", startTestFromStep2);"""

if old_bind_nav in js:
    js = js.replace(old_bind_nav, new_bind_nav)
else:
    js = re.sub(
        r'bindStepNavigation\(\)\s*\{[\s\S]*?document\.getElementById\("btnStep2Next"\)\?\.addEventListener\("click",\s*\(\)\s*=>\s*this\.goToStep\(3\)\);',
        new_bind_nav,
        js,
        count=1
    )

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js)
print("[OK] mock-test.js patched.")
