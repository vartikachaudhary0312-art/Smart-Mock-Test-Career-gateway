"""
Remove top action header card from Step 2 in mock-test.html
"""

import os
import re

HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "mock-test.html"))

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove the top card section with Back to Mock Tests and Start Test
top_card_pattern = r'\s*<!-- Step 2 Top Action Header: Start Test & Back buttons accessible near the top -->\s*<div class="card-custom p-3 mb-4 bg-surface border">[\s\S]*?</div>\s*</div>\s*</div>'

html = re.sub(top_card_pattern, '', html, count=1)

# 2. Restore clean summary banner (remove btnStep2QuickStart wrapper)
clean_banner_pattern = r'<div class="d-flex align-items-center gap-3 flex-wrap">\s*(<div class="text-md-end flex-shrink-0">\s*<span class="text-muted small d-block">Available In Bank</span>\s*<span class="fw-bold fs-5 text-primary" id="cfgSubjectAvailableCount">100 Questions</span>\s*</div>)\s*<button class="btn btn-primary-custom px-4 d-none d-md-inline-flex align-items-center" id="btnStep2QuickStart" type="button">[\s\S]*?</button>\s*</div>'

html = re.sub(clean_banner_pattern, r'\1', html, count=1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("[OK] Top action card removed from Step 2.")

