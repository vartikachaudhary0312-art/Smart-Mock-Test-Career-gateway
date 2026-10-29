import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'js', 'career.js')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

# 1. Update categories footer
old_cat_footer = """            <div class="d-flex justify-content-between align-items-center pt-3 border-top">
              <span class="small text-muted">
                <i class="bi bi-patch-check-fill text-success me-1"></i><strong>${totalQ}</strong> MCQs Available
              </span>
              <span class="text-primary fw-semibold small">
                Explore Topics <i class="bi bi-arrow-right"></i>
              </span>
            </div>"""

new_cat_footer = """            <div class="d-flex justify-content-between align-items-center pt-3 border-top flex-wrap gap-2">
              <span class="small text-muted">
                <i class="bi bi-patch-check-fill text-success me-1"></i><strong>${totalQ}</strong> MCQs Available
              </span>
              <span class="text-primary fw-semibold small">
                Explore Topics <i class="bi bi-arrow-right"></i>
              </span>
            </div>"""

content_norm = content_norm.replace(old_cat_footer, new_cat_footer)

# 2. Update topics buttons
old_top_btns = """                <div class="d-flex gap-2">
                  <button type="button" class="btn btn-outline-custom btn-sm flex-fill" onclick="CareerPage.openTopicConfig('${topic.id}', 'practice')">
                    <i class="bi bi-mortarboard-fill me-1 text-primary"></i> Practice
                  </button>
                  <button type="button" class="btn btn-primary-custom btn-sm flex-fill" onclick="CareerPage.openTopicConfig('${topic.id}', 'timed')">
                    <i class="bi bi-clock-history me-1"></i> Timed Test
                  </button>
                </div>"""

new_top_btns = """                <div class="d-flex gap-2 flex-wrap">
                  <button type="button" class="btn btn-outline-custom btn-sm flex-fill" onclick="CareerPage.openTopicConfig('${topic.id}', 'practice')">
                    <i class="bi bi-mortarboard-fill me-1 text-primary"></i> Practice
                  </button>
                  <button type="button" class="btn btn-primary-custom btn-sm flex-fill" onclick="CareerPage.openTopicConfig('${topic.id}', 'timed')">
                    <i class="bi bi-clock-history me-1"></i> Timed Test
                  </button>
                </div>"""

content_norm = content_norm.replace(old_top_btns, new_top_btns)

# 3. Update jobs buttons
old_job_btns = """            <div class="d-flex gap-2 border-top pt-3">
              <button class="btn btn-outline-custom btn-sm flex-grow-1" onclick="CareerPage.openJobDetails('${job.id}')">View Details</button>
              <button class="btn btn-primary-custom btn-sm flex-grow-1" onclick="CareerPage.openApplyModal('${job.id}')">Apply Now</button>
            </div>"""

new_job_btns = """            <div class="d-flex gap-2 border-top pt-3 flex-wrap">
              <button class="btn btn-outline-custom btn-sm flex-grow-1" onclick="CareerPage.openJobDetails('${job.id}')">View Details</button>
              <button class="btn btn-primary-custom btn-sm flex-grow-1" onclick="CareerPage.openApplyModal('${job.id}')">Apply Now</button>
            </div>"""

content_norm = content_norm.replace(old_job_btns, new_job_btns)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("SUCCESS: career.js patched successfully!")

