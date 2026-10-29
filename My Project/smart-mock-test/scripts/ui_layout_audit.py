import os
import re
import glob

frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
html_files = glob.glob(os.path.join(frontend_dir, '**', '*.html'), recursive=True)
js_files = glob.glob(os.path.join(frontend_dir, '**', '*.js'), recursive=True)
css_files = glob.glob(os.path.join(frontend_dir, '**', '*.css'), recursive=True)

print("=" * 60)
print("AUDIT 1: CSS Grid containers in CSS")
print("=" * 60)
for cf in css_files:
    with open(cf, 'r', encoding='utf-8') as f:
        content = f.read()
    for m in re.finditer(r'([^{}]+)\{([^{}]*display\s*:\s*grid[^{}]*)\}', content, re.DOTALL):
        sel = m.group(1).strip()
        body = m.group(2).strip()
        print(f"[{os.path.basename(cf)}] Selector: {sel}\n  Body: {body[:120]}...\n")

print("=" * 60)
print("AUDIT 2: HTML elements combining .row with other custom classes")
print("=" * 60)
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    # find class="..." with row
    matches = re.finditer(r'class=["\']([^"\']*\brow\b[^"\']*)["\']', content)
    for m in matches:
        cls_str = m.group(1)
        tokens = cls_str.split()
        custom = [t for t in tokens if not any(t.startswith(prefix) for prefix in [
            'row', 'g-', 'gx-', 'gy-', 'align-', 'justify-', 'my-', 'mb-', 'mt-', 'mx-',
            'py-', 'pb-', 'pt-', 'px-', 'p-', 'm-', 'text-', 'border', 'shadow', 'bg-',
            'd-', 'w-', 'h-', 'col-'
        ])]
        if custom:
            print(f"[{os.path.basename(hf)}] row with custom classes {custom}: class='{cls_str}'")

print("=" * 60)
print("AUDIT 3: JS templates combining .row with other custom classes")
print("=" * 60)
for jf in js_files:
    with open(jf, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.finditer(r'class=["\']([^"\']*\brow\b[^"\']*)["\']', content)
    for m in matches:
        cls_str = m.group(1)
        tokens = cls_str.split()
        custom = [t for t in tokens if not any(t.startswith(prefix) for prefix in [
            'row', 'g-', 'gx-', 'gy-', 'align-', 'justify-', 'my-', 'mb-', 'mt-', 'mx-',
            'py-', 'pb-', 'pt-', 'px-', 'p-', 'm-', 'text-', 'border', 'shadow', 'bg-',
            'd-', 'w-', 'h-', 'col-'
        ])]
        if custom:
            print(f"[{os.path.basename(jf)}] row with custom classes {custom}: class='{cls_str}'")

print("=" * 60)
print("AUDIT 4: Inappropriate word-break, overflow-wrap, white-space in CSS")
print("=" * 60)
for cf in css_files:
    with open(cf, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        if any(term in line for term in ['word-break', 'overflow-wrap', 'white-space', 'break-all', 'nowrap', 'text-overflow']):
            print(f"[{os.path.basename(cf)}:{idx}] {line.strip()}")

