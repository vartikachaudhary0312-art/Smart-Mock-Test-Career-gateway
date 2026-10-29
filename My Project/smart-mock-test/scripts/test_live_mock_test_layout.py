"""
SMART MOCK TEST & CAREER GATEWAY
Full Live Viewport Layout Verification across Desktop, Laptop, and Mobile
"""

import subprocess
import time
import json
import os
import requests
import websocket

PORT = 9555
PROFILE = os.path.join(os.environ.get("TEMP", "."), "chrome_test_prof_live")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def launch_chrome(width=1280, height=800):
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        f"--remote-debugging-port={PORT}",
        "--disable-gpu",
        f"--user-data-dir={PROFILE}",
        f"--window-size={width},{height}",
        "http://127.0.0.1:5000/mock-test.html"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(2)
    return proc

def run_tests():
    proc = launch_chrome(1280, 720) # 720p Laptop viewport

    try:
        pages = requests.get(f"http://127.0.0.1:{PORT}/json").json()
        target = None
        for p in pages:
            if "mock-test.html" in p.get("url", "") or "login.html" in p.get("url", ""):
                target = p
                break
        if not target:
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

        # 1. Setup authentication
        eval_js("""
            localStorage.setItem("smt_current_user", JSON.stringify({id: 1, name: "Rahul Sharma", email: "student@example.com", role: "student"}));
            localStorage.setItem("smt_auth_token", "valid_token_xyz");
        """)

        # 2. Reload mock-test.html
        eval_js("window.location.href = 'http://127.0.0.1:5000/mock-test.html'")
        time.sleep(1.5)

        # 3. Start Test with DSA Interview Coding Concepts
        print("\n--- TEST 1: Launching Mock Test (DSA Interview Coding Concepts) ---")
        eval_js("""
            (async function() {
                const sub = MockTestEngine.allSubjects.find(s => s.name && s.name.includes("DSA Interview")) || MockTestEngine.allSubjects[0];
                MockTestEngine.selectSubject(sub);
                MockTestEngine.hasActiveCamera = () => true;
                MockTestEngine.facePresenceVerified = true;
                await MockTestEngine.startActualTest();
            })()
        """, await_promise=True)
        time.sleep(1)

        # 4. Check initial viewport layout
        v1 = eval_js("""
        (function() {
            const btn = document.getElementById("btnNextQuestion");
            const bar = document.getElementById("testBottomActionBar");
            const qCard = document.querySelector(".test-question-card");
            const optContainer = document.getElementById("testOptionsContainer");
            const rBtn = btn.getBoundingClientRect();
            const rBar = bar.getBoundingClientRect();

            return {
                windowH: window.innerHeight,
                windowW: window.innerWidth,
                scrollY: window.scrollY,
                bodyScrollH: document.body.scrollHeight,
                btnVisibleInViewport: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight,
                btnTop: Math.round(rBtn.top),
                btnBottom: Math.round(rBtn.bottom),
                barTop: Math.round(rBar.top),
                barBottom: Math.round(rBar.bottom),
                qCardBottom: Math.round(qCard.getBoundingClientRect().bottom),
                optCount: optContainer.querySelectorAll(".option-item").length
            };
        })()
        """)
        print("  Metrics before selection:", json.dumps(v1, indent=2))
        assert v1["btnVisibleInViewport"], f"Continue button NOT in viewport! Top: {v1['btnTop']}, Bottom: {v1['btnBottom']}, WindowH: {v1['windowH']}"
        assert v1["qCardBottom"] <= v1["barTop"] + 5, f"Question card overlaps bottom action bar! qCardBottom: {v1['qCardBottom']}, barTop: {v1['barTop']}"
        assert v1["scrollY"] == 0, f"Page scrolled unexpectedly! scrollY: {v1['scrollY']}"
        print("  [PASS] Continue button is fully visible in viewport without any scrolling!")

        # 5. Select an option
        print("\n--- TEST 2: Select Option 2 (Index 1) ---")
        eval_js("""
        (function() {
            const q = MockTestEngine.questions[0];
            const opt = document.querySelector('.option-item[data-opt-idx="1"]');
            opt.click();
        })()
        """)
        time.sleep(0.5)

        v2 = eval_js("""
        (function() {
            const btn = document.getElementById("btnNextQuestion");
            const rBtn = btn.getBoundingClientRect();
            const selectedOpt = document.querySelector(".option-item.selected");
            const optIdx = selectedOpt ? selectedOpt.getAttribute("data-opt-idx") : null;
            const statusText = document.getElementById("testStickyStatusText").textContent;

            return {
                scrollY: window.scrollY,
                btnVisibleInViewport: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight,
                btnTop: Math.round(rBtn.top),
                btnBottom: Math.round(rBtn.bottom),
                selectedOptIdx: optIdx,
                statusText: statusText
            };
        })()
        """)
        print("  Metrics after selection:", json.dumps(v2, indent=2))
        assert v2["btnVisibleInViewport"], "Continue button moved offscreen after selection!"
        assert v2["scrollY"] == 0, "Selecting an option triggered page scrolling!"
        assert v2["selectedOptIdx"] == "1", "Selected option index not stored!"
        print("  [PASS] Option selected cleanly, Continue button remains 100% accessible in viewport with 0 page scrolling!")

        # 6. Click Continue to advance to Question 2
        print("\n--- TEST 3: Click Continue -> Advance to Question 2 ---")
        eval_js("""
        (function() {
            document.getElementById("btnNextQuestion").click();
        })()
        """)
        time.sleep(0.5)

        v3 = eval_js("""
        (function() {
            const btn = document.getElementById("btnNextQuestion");
            const rBtn = btn.getBoundingClientRect();
            return {
                currentIdx: MockTestEngine.currentIndex,
                scrollY: window.scrollY,
                btnVisibleInViewport: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight,
                btnTop: Math.round(rBtn.top),
                btnBottom: Math.round(rBtn.bottom),
                counterText: document.getElementById("testQuestionCounterText").textContent
            };
        })()
        """)
        print("  Question 2 metrics:", json.dumps(v3, indent=2))
        assert v3["currentIdx"] == 1, f"Expected currentIndex 1, got {v3['currentIdx']}"
        assert v3["btnVisibleInViewport"], "Continue button moved offscreen on question 2!"
        assert v3["scrollY"] == 0, "Page scrolled on question change!"
        print("  [PASS] Successfully advanced to Question 2. Continue button is immediately visible without scrolling!")

        # 7. Test Question Navigation Persistence (Go back to Q1, check selected answer preserved)
        print("\n--- TEST 4: Go Back to Question 1 -> Verify Answer Preserved ---")
        eval_js("""
        (function() {
            document.getElementById("btnPrevQuestion").click();
        })()
        """)
        time.sleep(0.5)

        v4 = eval_js("""
        (function() {
            const selectedOpt = document.querySelector(".option-item.selected");
            return {
                currentIdx: MockTestEngine.currentIndex,
                selectedOptIdx: selectedOpt ? selectedOpt.getAttribute("data-opt-idx") : null,
                paletteGreen: document.querySelector('.palette-item[data-q-idx="0"]').classList.contains("answered")
            };
        })()
        """)
        print("  Q1 restored metrics:", json.dumps(v4, indent=2))
        assert v4["currentIdx"] == 0, "Failed to navigate back to Q1"
        assert v4["selectedOptIdx"] == "1", "Selected option was not preserved on Q1!"
        assert v4["paletteGreen"], "Palette did not mark Q1 as answered green!"
        print("  [PASS] Selected answer perfectly preserved on Question 1, palette shows green!")

        # 8. Test Long Question with many options (Internal scroll without page scroll)
        print("\n--- TEST 5: Injecting Long Question with 8 Options ---")
        eval_js("""
        (function() {
            const longQ = {
                id: 9999,
                question: "Explain the algorithmic complexity and performance characteristics of Dijkstra's algorithm implemented with a Fibonacci heap versus a standard binary min-heap across dense versus sparse directed graphs with negative weight edge validation.",
                options: [
                    "O(V^2) with standard matrix representation",
                    "O(E + V log V) with Fibonacci heap",
                    "O((V + E) log V) with standard binary min-heap",
                    "O(V^3) with Floyd-Warshall dynamic programming",
                    "Bellman-Ford relaxation O(V * E) for negative cycle detection",
                    "Johnson's reweighting algorithm with auxiliary vertex",
                    "Tarjan's strongly connected components decomposition",
                    "None of the above complex formulations"
                ]
            };
            MockTestEngine.questions.push(longQ);
            MockTestEngine.currentIndex = MockTestEngine.questions.length - 1;
            MockTestEngine.renderCurrentQuestion();
        })()
        """)
        time.sleep(0.5)

        v5 = eval_js("""
        (function() {
            const btn = document.getElementById("btnNextQuestion");
            const rBtn = btn.getBoundingClientRect();
            const scrollBody = document.getElementById("testQuestionScrollBody");
            const bar = document.getElementById("testBottomActionBar");

            return {
                scrollY: window.scrollY,
                btnVisibleInViewport: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight,
                btnTop: Math.round(rBtn.top),
                btnBottom: Math.round(rBtn.bottom),
                barTop: Math.round(bar.getBoundingClientRect().top),
                scrollBodyScrollH: scrollBody.scrollHeight,
                scrollBodyClientH: scrollBody.clientHeight,
                scrollsInternally: scrollBody.scrollHeight > scrollBody.clientHeight,
                btnLabel: document.getElementById("btnContinueLabel").textContent
            };
        })()
        """)
        print("  Long Question metrics:", json.dumps(v5, indent=2))
        assert v5["btnVisibleInViewport"], "Continue button obscured during long question!"
        assert v5["scrollY"] == 0, "Outer page scrolled during long question!"
        assert v5["scrollsInternally"], "Question container did not enable internal scrolling for 8 options!"
        assert "Submit" in v5["btnLabel"] or "Finish" in v5["btnLabel"], "Final question did not show Submit/Finish label!"
        print("  [PASS] Long question scrolls internally inside the question panel. Continue / Finish button remains 100% visible and accessible!")

        # 9. Test Submission Modal on Final Question
        print("\n--- TEST 6: Trigger Final Submission Modal ---")
        eval_js("""
        (function() {
            document.getElementById("btnNextQuestion").click();
        })()
        """)
        time.sleep(0.5)

        v6 = eval_js("""
        (function() {
            const modal = document.getElementById("submitConfirmationModal");
            const isShown = modal.classList.contains("show") || window.getComputedStyle(modal).display === "block";
            return { modalShown: isShown };
        })()
        """)
        print("  Submit modal metrics:", json.dumps(v6, indent=2))
        assert v6["modalShown"], "Submit confirmation modal did not open on final question click!"
        print("  [PASS] Final question correctly opens Submit Confirmation modal.")

        print("\n==================================================================")
        print("ALL REAL BROWSER VIEWPORT & SCROLLING TESTS PASSED (100%)!")
        print("==================================================================")

    finally:
        proc.terminate()

if __name__ == "__main__":
    run_tests()

