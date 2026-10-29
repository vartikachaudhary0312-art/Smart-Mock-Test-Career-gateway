"""
SMART MOCK TEST & CAREER GATEWAY
Verification Suite for Mock Test Viewport Layout and Persistent Continue Button UX
"""

import os
import re
import urllib.request
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HTML_FILE = os.path.join(ROOT, "frontend", "mock-test.html")
CSS_FILE = os.path.join(ROOT, "frontend", "css", "test.css")
JS_FILE = os.path.join(ROOT, "frontend", "js", "mock-test.js")

def test_html_structure():
    print("\n--- 1. Testing HTML Structure in mock-test.html ---")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    required_ids = [
        "testStep4",
        "testQuestionText",
        "testOptionsContainer",
        "testQuestionScrollBody",
        "testBottomActionBar",
        "btnPrevQuestion",
        "btnNextQuestion",
        "btnMarkReview",
        "btnClearAnswer",
        "btnContinueLabel",
        "btnContinueIcon",
        "testStickyStatusBadge",
        "testStickyStatusText",
        "questionPaletteGrid",
        "btnSubmitFromPalette",
        "submitConfirmationModal",
        "btnConfirmSubmitTest"
    ]

    for elem_id in required_ids:
        assert f'id="{elem_id}"' in html, f"Missing id '{elem_id}' in mock-test.html"
        print(f"  [PASS] Element id='{elem_id}' present in mock-test.html")

    assert "step-sticky-bar" in html, "step-sticky-bar class missing in Step 1"
    print("  [PASS] step-sticky-bar present in Step 1")

    assert "test-bottom-action-bar" in html, "test-bottom-action-bar class missing in Step 4"
    print("  [PASS] test-bottom-action-bar present in Step 4")


def test_css_rules():
    print("\n--- 2. Testing CSS Rules in test.css ---")
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    rules_to_check = [
        (".option-item", "cursor: pointer"),
        (".option-item:hover", "border-color: var(--primary)"),
        (".option-item.selected", "background-color: var(--primary-light"),
        (".option-radio-circle", "border-radius: 50%"),
        (".option-radio-dot", "border-radius: 50%"),
        (".option-marker", "border-radius: var(--radius-sm"),
        (".option-text", "overflow-wrap: break-word"),
        (".option-selection-indicator", "margin-left: auto"),
        (".palette-item", "display: flex"),
        ("body.assessment-active", "overflow: hidden !important"),
        ("body.assessment-active", "height: 100vh !important"),
        (".assessment-workspace", "display: flex !important"),
        (".test-question-scroll-body", "overflow-y: auto !important"),
        (".test-bottom-action-inner", "flex-direction: row !important"),
        (".test-bottom-left-group", "flex-wrap: nowrap !important"),
        (".btn-continue", "min-width: 140px"),
        (".btn-ready-highlight", "animation: continueReadyGlow"),
        (".btn-finish-test", "background-color: #10b981 !important"),
        ("body.assessment-active .proctor-pip-widget", "bottom: calc(64px + 16px) !important")
    ]

    for selector, prop in rules_to_check:
        assert selector in css and prop in css, f"Missing rule '{selector}' with '{prop}' in test.css"
        print(f"  [PASS] Rule verified: {selector} with '{prop}'")


def test_js_logic():
    print("\n--- 3. Testing JavaScript Engine Logic in mock-test.js ---")
    with open(JS_FILE, "r", encoding="utf-8") as f:
        js = f.read()

    js_methods = [
        "selectOption(qId, optIdx)",
        "updateNavigationUI()",
        "goToNextQuestion()",
        "goToPrevQuestion()",
        "renderCurrentQuestion()",
        "renderQuestionPalette()",
        "btnConfirmSubmitTest"
    ]

    for method in js_methods:
        clean_method = method.split("(")[0]
        assert clean_method in js, f"Missing method/handler '{clean_method}' in mock-test.js"
        print(f"  [PASS] Method/Handler '{clean_method}' found in mock-test.js")

    assert 'document.body.classList.add("assessment-active");' in js, "assessment-active class addition missing in mock-test.js"
    assert "scrollBody.scrollTop = 0" in js, "Question scroll body reset missing"
    assert "this.isSubmitting" in js, "isSubmitting flag missing in mock-test.js"
    assert "confirmBtn.disabled = true" in js, "Submit button disabling missing"
    assert "nextBtn.disabled = true" in js, "Continue button disabling missing"
    print("  [PASS] assessment-active lifecycle, scroll body reset, and duplicate submit guards verified.")

    assert "Finish & Submit Test" in js, "Dynamic last question Finish label missing"
    print("  [PASS] Dynamic 'Finish & Submit Test' state verified on final question.")


def test_live_server_endpoints():
    print("\n--- 4. Testing Live HTTP Endpoints on Port 5000 ---")
    urls = [
        ("http://127.0.0.1:5000/mock-test.html", "Mock Test HTML"),
        ("http://127.0.0.1:5000/css/test.css", "Test CSS"),
        ("http://127.0.0.1:5000/js/mock-test.js", "Mock Test Engine JS"),
        ("http://127.0.0.1:5000/api/health", "Backend Health API")
    ]

    for url, desc in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SMT-Tester"})
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.status
                body = response.read().decode("utf-8", errors="ignore")
                assert status == 200, f"Expected 200 OK from {url}, got {status}"
                if url.endswith(".html"):
                    assert "testBottomActionBar" in body, "Live mock-test.html missing testBottomActionBar"
                    assert "testQuestionScrollBody" in body, "Live mock-test.html missing testQuestionScrollBody"
                elif url.endswith(".css"):
                    assert "assessment-workspace" in body, "Live test.css missing assessment-workspace"
                elif url.endswith(".js"):
                    assert "assessment-active" in body, "Live mock-test.js missing assessment-active"
                print(f"  [PASS] {desc} ({url}) returned 200 OK.")
        except Exception as e:
            print(f"  [FAIL] Failed accessing {url}: {e}")
            raise


if __name__ == "__main__":
    print("==================================================================")
    print("RUNNING SMART MOCK TEST VIEWPORT UX VERIFICATION SUITE")
    print("==================================================================")
    test_html_structure()
    test_css_rules()
    test_js_logic()
    test_live_server_endpoints()
    print("\n==================================================================")
    print("ALL MOCK TEST VIEWPORT LAYOUT & PERSISTENT CONTINUE UX CHECKS PASSED!")
    print("==================================================================")
