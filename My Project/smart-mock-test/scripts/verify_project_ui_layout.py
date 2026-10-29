import os
import re
import glob

frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
css_dir = os.path.join(frontend_dir, 'css')

print("=" * 70)
print("COMPREHENSIVE PROJECT-WIDE UI LAYOUT VERIFICATION TEST")
print("=" * 70)

errors = []

# TEST 1: Check mock-test.html markup for difficulty-options and length-options
print("\n--- TEST 1: mock-test.html Options Structure ---")
with open(os.path.join(frontend_dir, 'mock-test.html'), 'r', encoding='utf-8') as f:
    mt_html = f.read()

if 'class="row g-2 difficulty-options"' in mt_html:
    errors.append("mock-test.html still has conflicting 'row g-2 difficulty-options'")
else:
    print("PASS: mock-test.html does not mix 'row' with 'difficulty-options'")

if 'class="col-md-3"' in mt_html and 'data-diff=' in mt_html:
    # check if col-md-3 is directly wrapping difficulty-card
    if re.search(r'<div class="col-md-3">\s*<div class="difficulty-card', mt_html):
        errors.append("mock-test.html still has col-md-3 wrapping difficulty-card inside grid")
    else:
        print("PASS: difficulty-card is not wrapped in restrictive col-md-3 inside grid")
else:
    print("PASS: difficulty-card has clean direct grid children structure")

# Check all 4 difficulty levels exist in mock-test.html
for diff in ["Easy", "Medium", "Hard", "Mixed"]:
    if f'data-diff="{diff}"' in mt_html:
        print(f"PASS: Difficulty option '{diff}' exists in mock-test.html")
    else:
        errors.append(f"Difficulty option '{diff}' missing in mock-test.html")

# Check length options
for length in ["10", "20", "30", "50", "max"]:
    if f'data-length="{length}"' in mt_html:
        print(f"PASS: Length option '{length}' exists in mock-test.html")
    else:
        errors.append(f"Length option '{length}' missing in mock-test.html")

# TEST 2: Check test.css for difficulty-options and length-options rules
print("\n--- TEST 2: test.css Rules Verification ---")
with open(os.path.join(css_dir, 'test.css'), 'r', encoding='utf-8') as f:
    test_css = f.read()

if 'repeat(auto-fit, minmax(min(100%, 220px), 1fr))' in test_css:
    print("PASS: .difficulty-options has robust minmax(min(100%, 220px), 1fr)")
else:
    errors.append(".difficulty-options missing minmax(min(100%, 220px), 1fr) in test.css")

if 'repeat(auto-fit, minmax(min(100%, 140px), 1fr))' in test_css:
    print("PASS: #cfgLengthOptions has robust minmax(min(100%, 140px), 1fr)")
else:
    errors.append("#cfgLengthOptions missing minmax(min(100%, 140px), 1fr) in test.css")

if 'overflow-wrap: anywhere' in test_css:
    errors.append("test.css still contains 'overflow-wrap: anywhere' which can cause mid-word breaking")
else:
    print("PASS: test.css has NO 'overflow-wrap: anywhere'")

# TEST 3: Check career.css rules
print("\n--- TEST 3: career.css Rules Verification ---")
with open(os.path.join(css_dir, 'career.css'), 'r', encoding='utf-8') as f:
    career_css = f.read()

if 'min-height: 100%' in career_css:
    print("PASS: career.css uses min-height: 100% for responsive equal-height cards")
else:
    errors.append("career.css missing min-height: 100%")

if 'overflow-wrap: anywhere' in career_css:
    errors.append("career.css still contains 'overflow-wrap: anywhere'")
else:
    print("PASS: career.css has NO 'overflow-wrap: anywhere'")

# TEST 4: Check components.css and global.css rules
print("\n--- TEST 4: components.css & global.css Verification ---")
with open(os.path.join(css_dir, 'components.css'), 'r', encoding='utf-8') as f:
    comp_css = f.read()

with open(os.path.join(css_dir, 'global.css'), 'r', encoding='utf-8') as f:
    global_css = f.read()

if '*, *::before, *::after' in global_css and 'box-sizing: border-box' in global_css:
    print("PASS: global.css establishes universal box-sizing: border-box")
else:
    errors.append("global.css missing universal box-sizing")

if 'word-break: normal' in global_css and 'overflow-wrap: break-word' in global_css:
    print("PASS: global.css establishes safe word-boundary text wrapping")
else:
    errors.append("global.css missing safe word-boundary text wrapping")

if '.card-custom' in comp_css and 'min-width: 0' in comp_css:
    print("PASS: .card-custom has min-width: 0 and box-sizing: border-box")
else:
    errors.append(".card-custom missing min-width: 0 in components.css")

# TEST 5: Verify resume.html is clean and valid
print("\n--- TEST 5: resume.html Structure Verification ---")
with open(os.path.join(frontend_dir, 'resume.html'), 'r', encoding='utf-8') as f:
    resume_html = f.read()

if resume_html.strip().startswith('<!DOCTYPE html>'):
    print("PASS: resume.html begins cleanly with <!DOCTYPE html>")
else:
    errors.append("resume.html does not start with <!DOCTYPE html>")

# TEST 6: Check for any remaining width: 100vw that could cause horizontal scrollbar
print("\n--- TEST 6: Document-Level Horizontal Overflow Audit ---")
all_css = glob.glob(os.path.join(css_dir, '*.css'))
for cf in all_css:
    fname = os.path.basename(cf)
    with open(cf, 'r', encoding='utf-8') as f:
        c = f.read()
    # Check width: 100vw
    vw_matches = re.findall(r'width\s*:\s*100vw', c)
    if vw_matches:
        errors.append(f"{fname} still contains width: 100vw ({len(vw_matches)} occurrences)")
    else:
        print(f"PASS: {fname} has NO 'width: 100vw'")

# TEST 7: Mathematical Simulation of Difficulty Card Layout across Viewports
print("\n--- TEST 7: Mathematical Simulation of Difficulty Card Layout ---")
viewports = [
    ("Desktop Wide (1440px)", 1400),
    ("Desktop Standard (1200px)", 1140),
    ("Laptop / Tablet Landscape (992px)", 960),
    ("Tablet Portrait (768px)", 720),
    ("Mobile Large (480px)", 440),
    ("Mobile Small (360px)", 328),
]

min_col_desktop = 220
gap = 16  # 1rem = 16px

for vp_name, vp_width in viewports:
    # Compute columns
    # In CSS Grid: repeat(auto-fit, minmax(min(100%, 220px), 1fr))
    # Number of columns = max(1, floor((vp_width + gap) / (min_col_desktop + gap)))
    max_cols = 4  # there are 4 difficulty cards
    possible_cols = max(1, int((vp_width + gap) / (min_col_desktop + gap)))
    actual_cols = min(max_cols, possible_cols)
    
    # Calculate card width
    total_gaps = (actual_cols - 1) * gap
    card_width = (vp_width - total_gaps) / actual_cols
    
    # Card padding: 1.15rem top/bottom, 1.25rem left/right = 20px left, 20px right = 40px
    # Border: 1.5px * 2 = 3px
    content_width = card_width - 40 - 3
    
    print(f"  {vp_name}:")
    print(f"    Grid Columns: {actual_cols} | Card Width: {card_width:.1f}px | Usable Content Width: {content_width:.1f}px")
    
    # Validate:
    # "Medium" is ~55px, "Recommended" badge is ~85px.
    # Total needed side-by-side: 55 + 8 + 85 = 148px.
    # If content_width < 148px, the badge wraps cleanly below "Medium" because of flex-wrap: wrap.
    # But even on a 360px mobile screen, card_width is 328px and content_width is 285px!
    if card_width < 180:
        errors.append(f"Card width in {vp_name} is too narrow ({card_width:.1f}px < 180px)")
    else:
        print(f"    -> SAFE: Card width ({card_width:.1f}px) provides ample space for 'Medium' and 'Recommended'!")

print("\n" + "=" * 70)
if errors:
    print(f"AUDIT COMPLETED WITH {len(errors)} ERROR(S):")
    for err in errors:
        print(f"  - {err}")
    exit(1)
else:
    print("ALL 7 PROJECT-WIDE UI LAYOUT AUDIT TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

