"""
Script to apply comprehensive card layout and text overflow fixes across:
- frontend/css/test.css
- frontend/js/mock-test.js
- frontend/mock-test.html
- frontend/css/career.css
- frontend/js/career.js
- frontend/css/responsive.css
"""
import os
import re

BASE_DIR = os.path.abspath("My Project/smart-mock-test")

# 1. Update frontend/css/test.css
test_css_path = os.path.join(BASE_DIR, "frontend", "css", "test.css")
with open(test_css_path, "r", encoding="utf-8") as f:
    test_css = f.read()

# Replace the initial .subject-grid and .subject-card rules
old_card_css = """/* Mock Test Flow Styles */
.subject-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1.25rem;
}

.subject-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

.subject-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.subject-card.selected {
  border-color: var(--primary);
  background-color: var(--primary-light);
  box-shadow: var(--shadow-purple);
  transform: translateY(-2px);
}"""

new_card_css = """/* Mock Test Flow Styles */
.subject-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
  gap: 1.25rem;
  width: 100%;
}

.subject-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.35rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100%;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}

.subject-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.subject-card.selected {
  border-color: var(--primary);
  background-color: var(--primary-light);
  box-shadow: var(--shadow-purple);
  transform: translateY(-2px);
}

/* Card Content Body */
.subject-card-body {
  flex: 1 1 auto;
  min-width: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* Header: Icon + Info */
.subject-card-header {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  margin-bottom: 0.85rem;
  min-width: 0;
  width: 100%;
}

/* Stat Icon: Fixed size, never squished */
.subject-card .stat-icon-wrapper {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

/* Info Box: Shrinks inside flex container */
.subject-card-info {
  flex: 1 1 0%;
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
}

/* Title: Clean multi-line wrapping */
.subject-card-title {
  color: var(--text);
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.35;
  margin: 0;
  word-break: normal;
  overflow-wrap: break-word;
  word-wrap: break-word;
  max-width: 100%;
}

/* Badges: Wrap into multiple rows cleanly */
.subject-card-badges {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.35rem;
  margin-top: 0.4rem;
  min-width: 0;
  max-width: 100%;
}

.subject-card-badges .badge {
  white-space: normal !important;
  text-align: left;
  line-height: 1.25;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  font-size: 0.72rem;
  border-radius: var(--radius-sm);
  word-break: break-word;
  overflow-wrap: anywhere;
  max-width: 100%;
}

/* Description: Wraps cleanly */
.subject-card-desc {
  font-size: 0.84rem;
  line-height: 1.45;
  margin: 0;
  color: var(--muted);
  word-break: normal;
  overflow-wrap: break-word;
  word-wrap: break-word;
  max-width: 100%;
}

/* Footer: Neatly aligned with wrap capability */
.subject-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border);
  min-width: 0;
  width: 100%;
}

.subject-card-count {
  font-size: 0.82rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  min-width: 0;
  word-break: break-word;
  flex: 1 1 auto;
}

.subject-card-action {
  font-size: 0.84rem;
  font-weight: 600;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  flex-shrink: 0;
  margin-left: auto;
}"""

test_css = test_css.replace(old_card_css, new_card_css)
with open(test_css_path, "w", encoding="utf-8") as f:
    f.write(test_css)
print("Updated test.css with responsive card styling")

# 2. Update frontend/js/mock-test.js
mock_test_js_path = os.path.join(BASE_DIR, "frontend", "js", "mock-test.js")
with open(mock_test_js_path, "r", encoding="utf-8") as f:
    mt_js = f.read()

old_template = """      html += `
        <div class="subject-card ${isComingSoon ? 'opacity-75' : ''} ${isSelected ? 'selected' : ''}" 
             data-sub-id="${sub.id}" 
             data-sub-name="${sub.name}">
          <div>
            <div class="d-flex align-items-center gap-3 mb-3">
              <div class="stat-icon-wrapper stat-icon-purple">
                <i class="bi ${sub.icon || 'bi-journal-code'}"></i>
              </div>
              <div>
                <h6 class="fw-bold mb-0">${sub.name}</h6>
                <div class="d-flex gap-1 mt-1">
                  <span class="badge badge-secondary small">${sub.category || 'Core CS'}</span>
                  ${sub.code ? `<span class="badge bg-light text-dark border small">${sub.code}</span>` : ''}
                </div>
              </div>
            </div>
            <p class="text-muted small mb-0">${sub.description || 'Comprehensive CSE technical module covering conceptual & placement MCQs.'}</p>
          </div>
          <div class="d-flex justify-content-between align-items-center mt-3 pt-3 border-top">
            <span class="small ${isComingSoon ? 'text-warning' : 'text-muted'}">
              <i class="bi ${isComingSoon ? 'bi-hourglass-split' : 'bi-check-circle'} me-1 text-success"></i>${countLabel}
            </span>
            <span class="text-primary fw-semibold small">${isComingSoon ? 'Coming Soon' : 'Configure Test'} <i class="bi bi-chevron-right"></i></span>
          </div>
        </div>
      `;"""

new_template = """      html += `
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
      `;"""

if old_template in mt_js:
    mt_js = mt_js.replace(old_template, new_template)
    print("Replaced subject card template in mock-test.js")
else:
    # Check if lines differ by spacing/newlines
    print("Old template exact match not found in mock-test.js, checking regex...")
    pattern = re.compile(r'html\s*\+=\s*`\s*<div class="subject-card.*?</div>\s*</div>\s*`;', re.DOTALL)
    mt_js = pattern.sub(new_template, mt_js, count=1)
    print("Replaced via regex in mock-test.js")

with open(mock_test_js_path, "w", encoding="utf-8") as f:
    f.write(mt_js)

# 3. Update frontend/mock-test.html Step 2 summary card
mock_test_html_path = os.path.join(BASE_DIR, "frontend", "mock-test.html")
with open(mock_test_html_path, "r", encoding="utf-8") as f:
    mt_html = f.read()

old_step2_banner = """            <!-- Selected Subject Summary Banner -->
            <div class="card-custom p-3 mb-4 bg-surface-subtle border">
              <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                <div class="d-flex align-items-center gap-3">
                  <div class="stat-icon-wrapper stat-icon-purple" id="cfgSubjectIconWrap">
                    <i class="bi bi-journal-code fs-4" id="cfgSubjectIcon"></i>
                  </div>
                  <div>
                    <h5 class="fw-bold mb-0 text-dark" id="cfgSubjectName">Select Subject</h5>
                    <div class="d-flex gap-1 mt-1">
                      <span class="badge badge-purple small" id="cfgSubjectCategory">Core Computer Science</span>
                      <span class="badge badge-secondary small ms-1" id="cfgSubjectCode">CS-01</span>
                    </div>
                  </div>
                </div>
                <div class="text-md-end">
                  <span class="text-muted small d-block">Available In Bank</span>
                  <span class="fw-bold fs-5 text-primary" id="cfgSubjectAvailableCount">100 Questions</span>
                </div>
              </div>
            </div>"""

new_step2_banner = """            <!-- Selected Subject Summary Banner -->
            <div class="card-custom p-3 mb-4 bg-surface-subtle border">
              <div class="d-flex align-items-center justify-content-between flex-wrap gap-3">
                <div class="d-flex align-items-start gap-3 min-w-0 flex-grow-1">
                  <div class="stat-icon-wrapper stat-icon-purple flex-shrink-0" id="cfgSubjectIconWrap">
                    <i class="bi bi-journal-code fs-4" id="cfgSubjectIcon"></i>
                  </div>
                  <div class="min-w-0 flex-grow-1">
                    <h5 class="fw-bold mb-1 text-dark text-break" id="cfgSubjectName">Select Subject</h5>
                    <div class="d-flex flex-wrap gap-1 mt-1">
                      <span class="badge badge-purple small text-wrap text-start" id="cfgSubjectCategory">Core Computer Science</span>
                      <span class="badge badge-secondary small text-nowrap" id="cfgSubjectCode">CS-01</span>
                    </div>
                  </div>
                </div>
                <div class="text-md-end flex-shrink-0">
                  <span class="text-muted small d-block">Available In Bank</span>
                  <span class="fw-bold fs-5 text-primary" id="cfgSubjectAvailableCount">100 Questions</span>
                </div>
              </div>
            </div>"""

if old_step2_banner in mt_html:
    mt_html = mt_html.replace(old_step2_banner, new_step2_banner)
    with open(mock_test_html_path, "w", encoding="utf-8") as f:
        f.write(mt_html)
    print("Updated mock-test.html Step 2 summary banner")

# 4. Update frontend/css/career.css for topic cards
career_css_path = os.path.join(BASE_DIR, "frontend", "css", "career.css")
with open(career_css_path, "r", encoding="utf-8") as f:
    career_css = f.read()

enhanced_topic_css = """
/* Enhanced Card Title & Overflow Control */
.topic-card-title {
  word-break: normal;
  overflow-wrap: break-word;
  word-wrap: break-word;
  line-height: 1.35;
  margin: 0;
  max-width: 100%;
}

.topic-card-badge {
  white-space: normal;
  word-break: break-word;
}
"""

if "topic-card-title" not in career_css:
    career_css += "\n" + enhanced_topic_css
    with open(career_css_path, "w", encoding="utf-8") as f:
        f.write(career_css)
    print("Updated career.css with topic-card-title wrap rules")

# 5. Update frontend/js/career.js
career_js_path = os.path.join(BASE_DIR, "frontend", "js", "career.js")
with open(career_js_path, "r", encoding="utf-8") as f:
    career_js = f.read()

old_career_card_header = """              <div class="d-flex justify-content-between align-items-start mb-2">
                <div class="d-flex align-items-center gap-2">
                  <div class="subject-icon-box" style="background-color: ${this.activeCategory.bgColor || '#EEECFF'}; color: ${this.activeCategory.color || 'var(--primary)'};">
                    <i class="bi ${topic.icon || 'bi-journal-code'}"></i>
                  </div>
                  <div>
                    <h6 class="fw-bold text-dark mb-0">${topic.name}</h6>
                    <span class="badge badge-secondary" style="font-size: 0.7rem;">${topic.code || 'TOPIC'}</span>
                  </div>
                </div>
                ${isCompany ? `<span class="badge-pyq-notice"><i class="bi bi-patch-check-fill"></i> PYQ-Style</span>` : ''}
              </div>"""

new_career_card_header = """              <div class="d-flex justify-content-between align-items-start gap-2 mb-2 min-w-0">
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
              </div>"""

if old_career_card_header in career_js:
    career_js = career_js.replace(old_career_card_header, new_career_card_header)
    with open(career_js_path, "w", encoding="utf-8") as f:
        f.write(career_js)
    print("Updated career.js topic card header")

# 6. Update frontend/css/responsive.css
resp_css_path = os.path.join(BASE_DIR, "frontend", "css", "responsive.css")
with open(resp_css_path, "r", encoding="utf-8") as f:
    resp_css = f.read()

resp_card_rule = """
/* Responsive Subject Cards */
@media (max-width: 767.98px) {
  .subject-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .subject-card {
    padding: 1.15rem;
  }
}
"""

if "/* Responsive Subject Cards */" not in resp_css:
    resp_css += "\n" + resp_card_rule
    with open(resp_css_path, "w", encoding="utf-8") as f:
        f.write(resp_css)
    print("Updated responsive.css with single-column mobile grid rule")

print("All card layout and overflow fixes applied successfully!")
