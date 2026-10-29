import os
import re
import glob

frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
html_files = glob.glob(os.path.join(frontend_dir, '**', '*.html'), recursive=True)
js_files = glob.glob(os.path.join(frontend_dir, '**', '*.js'), recursive=True)
css_files = glob.glob(os.path.join(frontend_dir, '**', '*.css'), recursive=True)

print("=== 1. Searching for bg-white and bg-light in HTML and JS ===")
for f in html_files + js_files:
    fname = os.path.relpath(f, frontend_dir)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        for idx, line in enumerate(fp, 1):
            if re.search(r'\b(bg-white|bg-light)\b', line):
                print(f"[{fname}:{idx}] {line.strip()[:100]}")

print("\n=== 2. Searching for hardcoded hex colors in HTML and JS (inline styles or template literals) ===")
for f in html_files + js_files:
    fname = os.path.relpath(f, frontend_dir)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        for idx, line in enumerate(fp, 1):
            hexes = re.findall(r'#[0-9a-fA-F]{3,8}', line)
            # filter out common tokens like #landingNavbar or URL anchors
            real_hexes = [h for h in hexes if len(h) in [4, 7, 9]]
            if real_hexes and ('style=' in line or 'color' in line or 'background' in line):
                print(f"[{fname}:{idx}] {real_hexes} in: {line.strip()[:100]}")

print("\n=== 3. Searching for text-dark in HTML and JS ===")
count_td = 0
for f in html_files + js_files:
    fname = os.path.relpath(f, frontend_dir)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        for idx, line in enumerate(fp, 1):
            if 'text-dark' in line:
                count_td += 1
print(f"Total occurrences of 'text-dark': {count_td}")
