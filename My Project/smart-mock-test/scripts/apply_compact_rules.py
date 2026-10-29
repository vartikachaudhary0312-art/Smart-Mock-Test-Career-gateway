"""
SMART MOCK TEST & CAREER GATEWAY
Permanent Mock Test Layout & Navigation Fix
Refined padding & margins to eliminate dead whitespace and ensure Continue is 100% visible
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

# Change mb-4 on testQuestionText to mb-2.5
html = re.sub(
    r'<h5 class="fw-bold text-dark mb-4 lh-base" id="testQuestionText">',
    r'<h5 class="fw-bold text-dark mb-2.5 lh-base" id="testQuestionText">',
    html
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("[OK] mock-test.html updated.")

# ==========================================
# 2. PATCH test.css
# ==========================================
with open(CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()

# Compact assessment content inner padding
css = re.sub(
    r'\.assessment-content-inner\s*\{[^}]*\}',
    """.assessment-content-inner {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  display: flex !important;
  gap: 1rem !important;
  padding: 0.65rem 1.25rem !important;
  width: 100% !important;
  max-width: 1440px !important;
  margin: 0 auto !important;
  overflow: hidden !important;
}""",
    css,
    count=1
)

# Compact test-question-card padding
css = re.sub(
    r'\.assessment-question-col\s+\.test-question-card\s*\{[^}]*\}',
    """.assessment-question-col .test-question-card {
  height: 100% !important;
  max-height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
  overflow: hidden !important;
  padding: 0.95rem 1.25rem 0.5rem 1.25rem !important;
  margin-bottom: 0 !important;
}""",
    css,
    count=1
)

# Compact test-question-meta-header
css = re.sub(
    r'\.test-question-meta-header\s*\{[^}]*\}',
    """.test-question-meta-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  flex-shrink: 0;
}""",
    css,
    count=1
)

# Options container and option items compact rules
css = re.sub(
    r'/\* Options Container styling \*/[\s\S]*?\.test-options-container \.option-item\s*\{[^}]*\}',
    """/* Options Container styling */
.test-options-container {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.test-options-container .option-item {
  margin-bottom: 0 !important;
  padding: 0.55rem 0.95rem !important;
  gap: 0.75rem !important;
  border-radius: var(--radius-sm, 10px) !important;
}

.test-options-container .option-marker {
  width: 28px !important;
  height: 28px !important;
  font-size: 0.82rem !important;
}

.test-options-container .option-radio-circle {
  width: 20px !important;
  height: 20px !important;
}""",
    css,
    count=1
)

# Toolbar compact rule
css = re.sub(
    r'\.test-question-actions-toolbar,\s*\.assessment-workspace \.test-bottom-action-bar\s*\{[^}]*\}',
    """.test-question-actions-toolbar,
.assessment-workspace .test-bottom-action-bar {
  flex-shrink: 0 !important;
  position: relative !important;
  background-color: var(--surface) !important;
  border-top: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 0.55rem 0.5rem 0.2rem 0.5rem !important;
  margin-top: 0.75rem !important;
  margin-bottom: 0.25rem !important;
  z-index: 10 !important;
  box-shadow: none !important;
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
}""",
    css,
    count=1
)

with open(CSS_PATH, "w", encoding="utf-8") as f:
    f.write(css)
print("[OK] test.css updated with compact responsive rules.")

