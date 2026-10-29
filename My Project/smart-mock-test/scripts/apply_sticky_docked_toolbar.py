"""
SMART MOCK TEST & CAREER GATEWAY
Sticky Docked Action Bar with Safe Bottom Padding
Guarantees 100% accessibility on Laptop and Mobile viewports without overlap
"""

import os
import re

CSS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "css", "test.css"))

with open(CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update .test-question-scroll-body to include safe bottom padding for sticky bar
css = re.sub(
    r'\.test-question-scroll-body\s*\{[^}]*\}',
    """.test-question-scroll-body {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  padding-right: 0.5rem !important;
  padding-bottom: 72px !important;
  display: flex !important;
  flex-direction: column !important;
  position: relative !important;
}""",
    css,
    count=1
)

# 2. Update .test-question-actions-toolbar to be sticky at bottom: 0 with crisp shadow
css = re.sub(
    r'\.test-question-actions-toolbar,\s*\.assessment-workspace \.test-bottom-action-bar\s*\{[^}]*\}',
    """.test-question-actions-toolbar,
.assessment-workspace .test-bottom-action-bar {
  flex-shrink: 0 !important;
  position: sticky !important;
  bottom: 0 !important;
  background-color: var(--surface) !important;
  border-top: 1px solid var(--border) !important;
  border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
  padding: 0.55rem 0.75rem !important;
  margin-top: auto !important;
  margin-bottom: 0 !important;
  z-index: 30 !important;
  box-shadow: 0 -4px 14px rgba(0, 0, 0, 0.06) !important;
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
}""",
    css,
    count=1
)

# 3. Enhance mobile media query for ultra-clean fitting
mobile_media_target = r'@media\s*\(max-width:\s*991\.98px\)\s*\{[\s\S]*?body\.assessment-active\s+\.proctor-pip-widget\s*\{[^}]*\}\s*\}'

mobile_media_replacement = """@media (max-width: 991.98px) {
  .assessment-workspace .test-header-bar {
    padding: 0.35rem 0.75rem !important;
    height: auto !important;
    min-height: 44px !important;
  }

  .assessment-workspace .test-header-bar .badge {
    font-size: 0.68rem !important;
    padding: 0.2rem 0.45rem !important;
  }

  .assessment-workspace .timer-badge {
    font-size: 0.95rem !important;
    padding: 0.25rem 0.6rem !important;
  }

  .assessment-content-inner {
    flex-direction: column !important;
    gap: 0.5rem !important;
    padding: 0.5rem !important;
  }

  .assessment-palette-col {
    display: none !important;
  }

  .assessment-question-col {
    flex: 1 1 100% !important;
    height: 100% !important;
    min-height: 0 !important;
  }

  .assessment-question-col .test-question-card {
    padding: 0.65rem 0.75rem 0 0.75rem !important;
  }

  .test-options-container .option-item {
    padding: 0.45rem 0.75rem !important;
    font-size: 0.88rem !important;
  }

  .test-question-actions-toolbar,
  .assessment-workspace .test-bottom-action-bar {
    padding: 0.45rem 0.5rem !important;
  }

  .btn-continue {
    min-width: 100px !important;
    padding: 0.35rem 0.9rem !important;
    font-size: 0.85rem !important;
  }

  body.assessment-active .proctor-pip-widget {
    bottom: calc(56px + 10px) !important;
    right: 12px !important;
    width: 120px !important;
    height: 90px !important;
  }
}"""

css = re.sub(mobile_media_target, mobile_media_replacement, css, count=1)

with open(CSS_PATH, "w", encoding="utf-8") as f:
    f.write(css)

print("[OK] test.css updated with sticky docked toolbar and mobile refinements.")

