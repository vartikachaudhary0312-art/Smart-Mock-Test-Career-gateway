import os
import re
import glob

frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
html_files = glob.glob(os.path.join(frontend_dir, '**', '*.html'), recursive=True)
js_files = glob.glob(os.path.join(frontend_dir, '**', '*.js'), recursive=True)

print("=== SCAN 1: All elements with col- classes and their parent container classes ===")
col_pattern = re.compile(r'<div[^>]*class=["\']([^"\']*\bcol(?:-[a-zA-Z0-9]+)*\b[^"\']*)["\']', re.IGNORECASE)

for hf in html_files:
    fname = os.path.relpath(hf, frontend_dir)
    with open(hf, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # We can trace parent tags by looking at stack or regex
    for idx, line in enumerate(lines):
        if 'col-' in line or 'col"' in line or 'col ' in line or "col'" in line:
            # Check previous 5 lines for parent container
            prev_context = "".join(lines[max(0, idx-4):idx])
            parent_match = re.findall(r'<div[^>]*class=["\']([^"\']*)["\']', prev_context)
            if parent_match:
                parent_cls = parent_match[-1]
                # Check if parent has grid or custom class
                if 'grid' in parent_cls or 'options' in parent_cls or 'card' in parent_cls:
                    print(f"[{fname}:{idx+1}] Parent has suspicious class: '{parent_cls}'\n  Child: {line.strip()[:100]}")

print("\n=== SCAN 2: Checking #cfgLengthOptions in mock-test.html ===")
with open(os.path.join(frontend_dir, 'mock-test.html'), 'r', encoding='utf-8') as f:
    mt_content = f.read()

cfg_len = re.search(r'id=["\']cfgLengthOptions["\'][^>]*>(.*?)</div>\s*</div>', mt_content, re.DOTALL)
if cfg_len:
    print("Found cfgLengthOptions structure:")
    print(cfg_len.group(0)[:300])

print("\n=== SCAN 3: Checking all difficulty / config selectors across project ===")
for hf in html_files:
    fname = os.path.relpath(hf, frontend_dir)
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'difficulty' in content.lower():
        matches = re.finditer(r'([^\n]*difficulty[^\n]*)', content, re.IGNORECASE)
        for m in list(matches)[:5]:
            print(f"[{fname}] {m.group(1).strip()[:100]}")

