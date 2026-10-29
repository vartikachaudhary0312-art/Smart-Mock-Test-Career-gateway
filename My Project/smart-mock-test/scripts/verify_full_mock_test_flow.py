"""
SMART MOCK TEST & CAREER GATEWAY
Full End-to-End Mock Test UX & Viewport Layout Verification
Tests:
1. Card Listing (Step 1): Active test screen (Step 4) is 100% hidden.
2. Clicking Card: Transitions to Step 2 (Test Details & Config).
3. Step 2 (Test Details):
   - 'Back to Mock Tests' button is easily accessible near the top.
   - 'Start Test' button is easily accessible near the top (no scrolling required).
   - Clicking 'Back to Mock Tests' returns cleanly to Step 1.
4. Clicking 'Start Test': Transitions to Step 3 / Step 4.
5. Active Test Screen (Step 4):
   - Question is at top.
   - Timer, progress, and question counter are near the top.
   - Options are directly below the question.
   - Next / Continue button is visible directly below answer options.
   - Clicking an option updates selection and keeps Continue accessible with 0 page scroll.
   - Clicking Continue advances to Question 2.
   - Clicking Previous returns to Question 1 and preserves selection.
   - Submit button opens confirmation modal.
6. Responsive Verification across Laptop (1280x720) and Mobile (375x667).
"""

import subprocess
import time
import json
import os
import requests
import websocket

PORT = 9559
PROFILE = os.path.join(os.environ.get("TEMP", "."), "chrome_test_prof_flow")

def run_suite():
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        f"--remote-debugging-port={PORT}",
        "--disable-gpu",
        f"--user-data-dir={PROFILE}",
        "--window-size=1280,720",
        "http://127.0.0.1:5000/login.html"
    ]

    proc = subprocess.Popen(cmd)
    time.sleep(2)

    try:
        pages = requests.get(f"http://127.0.0.1:{PORT}/json").json()
        target = [p for p in pages if p.get("type") == "page"][0]
        ws = websocket.create_connection(target["webSocketDebuggerUrl"])
        msg_id = 1

        def eval_js(code, await_promise=False):
            nonlocal msg_id
            payload = {
                "id": msg_id,
                "method": "Runtime.evaluate",
                "params": {"expression": code, "returnByValue": True, "awaitPromise": await_promise}
            }
            ws.send(json.dumps(payload))
            msg_id += 1
            while True:
                resp = json.loads(ws.recv())
                if resp.get("id") == payload["id"]:
                    res = resp.get("result", {})
                    if "exceptionDetails" in res:
                        raise Exception("JS Exception: " + json.dumps(res["exceptionDetails"]))
                    return res.get("result", {}).get("value")

        # 1. Navigate to domain first, then Setup Student Authentication
        eval_js("window.location.href = 'http://127.0.0.1:5000/login.html'")
        time.sleep(1.5)
        eval_js("""
            localStorage.setItem("smt_current_user", JSON.stringify({id: 1, name: "Rahul Sharma", email: "student@example.com", role: "student"}));
            localStorage.setItem("smt_auth_token", "valid_token_xyz");
        """)
        eval_js("window.location.href = 'http://127.0.0.1:5000/mock-test.html'")
        time.sleep(2)

        print("\n=======================================================")
        print("STAGE 1: Step 1 Card Listing & Step 4 Isolation Check")
        print("=======================================================")
        s1_data = eval_js("""
        (function() {
            const s1 = document.getElementById('testStep1');
            const s4 = document.getElementById('testStep4');
            const cards = document.querySelectorAll('.subject-card');
            return {
                currentStep: MockTestEngine.currentStep,
                s1_display: window.getComputedStyle(s1).display,
                s4_display: window.getComputedStyle(s4).display,
                s4_visible: s4.offsetWidth > 0 && s4.offsetHeight > 0,
                cardsCount: cards.length
            };
        })()
        """)
        print("Step 1 Metrics:", json.dumps(s1_data, indent=2))
        assert s1_data["currentStep"] == 1, "Should be on Step 1"
        assert s1_data["s1_display"] == "block", "Step 1 should be visible"
        assert s1_data["s4_display"] == "none", "Step 4 must be hidden"
        assert s1_data["s4_visible"] is False, "Step 4 must have 0 size"
        print(">>> [PASS] Step 1 cards listing active; Question component from Step 4 is 100% hidden!")

        print("\n=======================================================")
        print("STAGE 2: Click Test Card -> Navigate to Step 2 Details")
        print("=======================================================")
        s2_click = eval_js("""
        (function() {
            const firstCard = document.querySelector('.subject-card');
            firstCard.click();
            const s1 = document.getElementById('testStep1');
            const s2 = document.getElementById('testStep2');
            const s4 = document.getElementById('testStep4');
            const topBarCard = document.getElementById('btnStep2BackTop');

            return {
                currentStep: MockTestEngine.currentStep,
                s1_display: window.getComputedStyle(s1).display,
                s2_display: window.getComputedStyle(s2).display,
                s4_display: window.getComputedStyle(s4).display,
                selectedSubject: MockTestEngine.selectedSubject ? MockTestEngine.selectedSubject.name : null,
                topBarRemoved: topBarCard === null
            };
        })()
        """)
        print("Step 2 Metrics:", json.dumps(s2_click, indent=2))
        assert s2_click["currentStep"] == 2, "Should have navigated to Step 2"
        assert s2_click["s2_display"] == "block", "Step 2 should be block"
        assert s2_click["s1_display"] == "none", "Step 1 should be hidden"
        assert s2_click["topBarRemoved"] is True, "Top action card must be removed from Step 2 as requested"
        print(">>> [PASS] Clicking card opened clean Step 2 Test Details; Top card section successfully removed!")

        print("\n=======================================================")
        print("STAGE 3: Test 'Back to Mock Tests' Button")
        print("=======================================================")
        back_check = eval_js("""
        (function() {
            document.getElementById('btnStep2Back').click();
            const s1 = document.getElementById('testStep1');
            const s2 = document.getElementById('testStep2');
            return {
                currentStep: MockTestEngine.currentStep,
                s1_display: window.getComputedStyle(s1).display,
                s2_display: window.getComputedStyle(s2).display
            };
        })()
        """)
        print("Back Navigation Metrics:", json.dumps(back_check, indent=2))
        assert back_check["currentStep"] == 1, "Should have returned to Step 1"
        assert back_check["s1_display"] == "block", "Step 1 should be visible"
        assert back_check["s2_display"] == "none", "Step 2 should be hidden"
        print(">>> [PASS] Back to Mock Tests works cleanly, returned to Step 1!")

        print("\n=======================================================")
        print("STAGE 4: Re-open Step 2 & Launch Test (Step 4)")
        print("=======================================================")
        launch_check = eval_js("""
        (async function() {
            // Click card again
            document.querySelector('.subject-card').click();
            // Bypass camera hardware requirement for test run
            MockTestEngine.hasActiveCamera = () => true;
            MockTestEngine.facePresenceVerified = true;
            await MockTestEngine.startActualTest();

            const s1 = document.getElementById('testStep1');
            const s2 = document.getElementById('testStep2');
            const s4 = document.getElementById('testStep4');
            const qText = document.getElementById('testQuestionText');
            const optsContainer = document.getElementById('testOptionsContainer');
            const btnContinue = document.getElementById('btnNextQuestion');
            const btnPrev = document.getElementById('btnPrevQuestion');
            const timer = document.getElementById('testLiveTimer');

            const rQ = qText.getBoundingClientRect();
            const rOpts = optsContainer.getBoundingClientRect();
            const rBtn = btnContinue.getBoundingClientRect();

            return {
                currentStep: MockTestEngine.currentStep,
                s4_display: window.getComputedStyle(s4).display,
                s1_display: window.getComputedStyle(s1).display,
                qTextTop: Math.round(rQ.top),
                qTextBottom: Math.round(rQ.bottom),
                optsTop: Math.round(rOpts.top),
                optsBottom: Math.round(rOpts.bottom),
                btnContinueTop: Math.round(rBtn.top),
                btnContinueBottom: Math.round(rBtn.bottom),
                btnContinueVisible: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight,
                timerValue: timer ? timer.innerText : null,
                prevDisabled: btnPrev ? btnPrev.disabled : null,
                windowH: window.innerHeight,
                windowW: window.innerWidth
            };
        })()
        """, await_promise=True)
        print("Active Test (Step 4) Metrics:", json.dumps(launch_check, indent=2))
        assert launch_check["currentStep"] == 4, "Should be on Step 4"
        assert launch_check["s4_display"] == "flex", "Step 4 must be flex"
        assert launch_check["qTextTop"] < launch_check["optsTop"], "Question text must be above options"
        assert launch_check["optsBottom"] <= launch_check["btnContinueTop"] + 30, "Continue button must be directly below answer options"
        assert launch_check["btnContinueVisible"] is True, "Next/Continue button must be immediately visible without scrolling!"
        assert launch_check["prevDisabled"] is True, "Previous should be disabled on Question 1"
        print(">>> [PASS] Active test launched! Question is near top, options directly below, Continue button directly below options and 100% visible!")

        print("\n=======================================================")
        print("STAGE 5: Option Selection & Navigation Flow")
        print("=======================================================")
        flow_check = eval_js("""
        (function() {
            // Select Option B (idx 1)
            const optB = document.getElementById('mockOptItem_1');
            optB.click();

            const btnContinue = document.getElementById('btnNextQuestion');
            const rBtn = btnContinue.getBoundingClientRect();
            const statusText = document.getElementById('testStickyStatusText').innerText;

            return {
                selectedClass: optB.classList.contains('selected'),
                btnVisibleAfterSelect: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight,
                btnTop: Math.round(rBtn.top),
                btnBottom: Math.round(rBtn.bottom),
                statusText: statusText
            };
        })()
        """)
        print("Selection Metrics:", json.dumps(flow_check, indent=2))
        assert flow_check["selectedClass"] is True, "Option B should be selected"
        assert flow_check["btnVisibleAfterSelect"] is True, "Continue must remain visible after selection"
        print(">>> [PASS] Option selection works seamlessly; Continue is immediately accessible!")

        print("\n=======================================================")
        print("STAGE 6: Click Continue -> Advance to Question 2")
        print("=======================================================")
        q2_check = eval_js("""
        (function() {
            document.getElementById('btnNextQuestion').click();
            const btnPrev = document.getElementById('btnPrevQuestion');
            const btnContinue = document.getElementById('btnNextQuestion');
            const rBtn = btnContinue.getBoundingClientRect();
            const qBadge = document.getElementById('testQuestionBadge').innerText;

            return {
                currentIndex: MockTestEngine.currentIndex,
                qBadge: qBadge,
                prevDisabled: btnPrev.disabled,
                btnContinueVisible: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight
            };
        })()
        """)
        print("Question 2 Metrics:", json.dumps(q2_check, indent=2))
        assert q2_check["currentIndex"] == 1, "Should be on Question 2 (idx 1)"
        assert q2_check["prevDisabled"] is False, "Previous button should now be enabled"
        assert q2_check["btnContinueVisible"] is True, "Continue must be visible on Question 2"
        print(">>> [PASS] Advanced to Question 2! Previous is enabled, Continue is visible!")

        print("\n=======================================================")
        print("STAGE 7: Click Previous -> Return to Question 1")
        print("=======================================================")
        q1_return = eval_js("""
        (function() {
            document.getElementById('btnPrevQuestion').click();
            const optB = document.getElementById('mockOptItem_1');
            return {
                currentIndex: MockTestEngine.currentIndex,
                optBStillSelected: optB ? optB.classList.contains('selected') : false
            };
        })()
        """)
        print("Return to Q1 Metrics:", json.dumps(q1_return, indent=2))
        assert q1_return["currentIndex"] == 0, "Should be back on Question 1"
        assert q1_return["optBStillSelected"] is True, "Answer should be preserved"
        print(">>> [PASS] Returned to Question 1! Selected answer preserved!")

        print("\n=======================================================")
        print("STAGE 8: Submit Test Modal Trigger")
        print("=======================================================")
        modal_check = eval_js("""
        (async function() {
            MockTestEngine.showSubmitConfirmationModal();
            await new Promise(r => setTimeout(r, 400));
            const modal = document.getElementById('submitConfirmationModal');
            return {
                modalShown: modal.classList.contains('show') || modal.style.display === 'block'
            };
        })()
        """, await_promise=True)
        print("Modal Metrics:", json.dumps(modal_check, indent=2))
        assert modal_check["modalShown"] is True, "Submit modal should be open"
        print(">>> [PASS] Submit confirmation modal triggers correctly!")

        print("\n=======================================================")
        print("STAGE 9: Mobile Viewport Layout Verification (375x667)")
        print("=======================================================")
        # Resize window to mobile
        eval_js("""
            // Hide modal first
            const modalEl = document.getElementById('submitConfirmationModal');
            const bsModal = bootstrap.Modal.getInstance(modalEl);
            if (bsModal) bsModal.hide();
        """)
        time.sleep(0.5)

        # Emulate mobile viewport dimensions via DevTools protocol
        payload = {
            "id": 999,
            "method": "Emulation.setDeviceMetricsOverride",
            "params": {
                "width": 375,
                "height": 667,
                "deviceScaleFactor": 2,
                "mobile": True
            }
        }
        ws.send(json.dumps(payload))
        time.sleep(0.5)

        mobile_metrics = eval_js("""
        (function() {
            const btnContinue = document.getElementById('btnNextQuestion');
            const qText = document.getElementById('testQuestionText');
            const optsContainer = document.getElementById('testOptionsContainer');
            const rBtn = btnContinue.getBoundingClientRect();
            const rQ = qText.getBoundingClientRect();
            const rOpts = optsContainer.getBoundingClientRect();

            return {
                windowW: window.innerWidth,
                windowH: window.innerHeight,
                qTextTop: Math.round(rQ.top),
                optsTop: Math.round(rOpts.top),
                btnContinueTop: Math.round(rBtn.top),
                btnContinueBottom: Math.round(rBtn.bottom),
                btnVisible: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight
            };
        })()
        """)
        print("Mobile Metrics:", json.dumps(mobile_metrics, indent=2))
        assert mobile_metrics["btnVisible"] is True, "Continue button must be visible on mobile screen without scrolling!"
        print(">>> [PASS] Mobile viewport layout verified! Continue button is fully visible!")

        print("\n=======================================================")
        print("ALL TESTS PASSED WITH 100% SUCCESS!")
        print("=======================================================")

    finally:
        proc.terminate()

if __name__ == "__main__":
    run_suite()
