import os
import re
import glob

frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
css_files = glob.glob(os.path.join(frontend_dir, 'css', '*.css'))

card_classes = [
    'subject-card',
    'subject-card-enhanced',
    'category-portal-card',
    'difficulty-card',
    'cfg-len-card',
    'config-option-card',
    'config-length-btn',
    'mode-select-card',
    'action-card',
    'stat-card',
    'card-custom',
    'job-card',
    'question-option-item',
    'practice-option-item',
    'question-review-item',
]

print("=== CSS RULES FOR ALL CARD TYPES ===")
for cf in css_files:
    fname = os.path.basename(cf)
    with open(cf, 'r', encoding='utf-8') as f:
        content = f.read()
    for cname in card_classes:
        pattern = rf'(\.{cname}\b[^{{}}]*\{{[^{{}}]*\}})'
        matches = re.findall(pattern, content)
        for m in matches:
            print(f"[{fname}] {m.strip()}\n")

