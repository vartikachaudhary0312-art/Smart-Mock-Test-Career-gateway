import os

# 1. Update mock-test.html
p_html = os.path.join("My Project", "smart-mock-test", "frontend", "mock-test.html")
with open(p_html, "r", encoding="utf-8") as f:
    c_html = f.read()

c_html = c_html.replace('class="test-bottom-action-inner content-max-width"', 'class="test-bottom-action-inner"')
with open(p_html, "w", encoding="utf-8") as f:
    f.write(c_html)
print("Updated mock-test.html")

# 2. Update test.css
p_css = os.path.join("My Project", "smart-mock-test", "frontend", "css", "test.css")
with open(p_css, "r", encoding="utf-8") as f:
    c_css = f.read()

target_css = """.assessment-workspace .test-bottom-action-inner {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  width: 100% !important;
  max-width: 1440px !important;
  margin: 0 auto !important;
}"""

new_css = """.test-bottom-action-inner,
.assessment-workspace .test-bottom-action-inner {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: nowrap !important;
  width: 100% !important;
  max-width: 1440px !important;
  margin: 0 auto !important;
  height: 100% !important;
}

/* Ensure left group items never wrap into a column inside the 64px bar */
.test-bottom-left-group {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 0.5rem !important;
  flex-wrap: nowrap !important;
}

.test-bottom-right-group {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 0.75rem !important;
  flex-wrap: nowrap !important;
}"""

c_css = c_css.replace(target_css, new_css)
with open(p_css, "w", encoding="utf-8") as f:
    f.write(c_css)
print("Updated test.css")

