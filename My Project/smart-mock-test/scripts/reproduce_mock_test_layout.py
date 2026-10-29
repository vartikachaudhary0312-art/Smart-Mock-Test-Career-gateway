"""
SMART MOCK TEST & CAREER GATEWAY
Headless Chrome Diagnostic Script: Reproduce and Measure Mock Test Layout
"""

import subprocess
import time
import json
import os
import requests
import websocket

PORT = 9444
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROFILE = os.path.join(os.environ.get("TEMP", "."), "chrome_test_profile_diag")

def run_diagnostics():
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        f"--remote-debugging-port={PORT}",
        "--disable-gpu",
        f"--user-data-dir={PROFILE}",
        "--window-size=1280,800",
        "http://127.0.0.1:5000/mock-test.html"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(2)

    try:
        pages = requests.get(f"http://127.0.0.1:{PORT}/json").json()
        target = None
        for p in pages:
            if "mock-test.html" in p.get("url", "") or "login.html" in p.get("url", ""):
                target = p
                break
        if not target:
            target = pages[0]

        ws_url = target["webSocketDebuggerUrl"]
        ws = websocket.create_connection(ws_url)

        msg_id = 1
        def send_cmd(method, params=None):
            nonlocal msg_id
            payload = {"id": msg_id, "method": method, "params": params or {}}
            ws.send(json.dumps(payload))
            msg_id += 1
            while True:
                resp = json.loads(ws.recv())
                if resp.get("id") == payload["id"]:
                    return resp.get("result", {})

        # 1. Inject student credentials into localStorage
        setup_script = """
        (function() {
            localStorage.setItem("smt_current_user", JSON.stringify({
                id: 1,
                name: "Rahul Sharma",
                email: "student@example.com",
                role: "student"
            }));
            localStorage.setItem("smt_auth_token", "test_student_token_123");
            return "Auth injected";
        })()
        """
        send_cmd("Runtime.evaluate", {"expression": setup_script})

        # 2. Navigate to mock-test.html
        send_cmd("Page.navigate", {"url": "http://127.0.0.1:5000/mock-test.html"})
        time.sleep(1.5)

        # 3. Start test with DSA Interview Coding Concepts
        start_test_script = """
        (async function() {
            // Find DSA subject
            const subs = MockTestEngine.allSubjects;
            let sub = subs.find(s => s.name && s.name.includes("DSA Interview"));
            if (!sub) sub = subs[0];

            MockTestEngine.selectSubject(sub);
            MockTestEngine.hasActiveCamera = () => true;
            MockTestEngine.facePresenceVerified = true;
            await MockTestEngine.startActualTest();

            // Select option 1 on current question
            const q = MockTestEngine.questions[0];
            MockTestEngine.selectOption(q.id, 1);

            return "Test started & option selected";
        })()
        """
        eval_res = send_cmd("Runtime.evaluate", {"expression": start_test_script, "awaitPromise": True})
        print("Start test result:", eval_res)
        time.sleep(1)

        # 4. Measure layout metrics
        measure_script = """
        (function() {
            const nextBtn = document.getElementById("btnNextQuestion");
            const bottomBar = document.getElementById("testBottomActionBar");
            const qCard = document.querySelector(".test-question-card");
            const optContainer = document.getElementById("testOptionsContainer");
            const testStep4 = document.getElementById("testStep4");
            const appMain = document.querySelector(".app-main");
            const pageBody = document.querySelector(".page-body");

            function getInfo(el) {
                if (!el) return null;
                const r = el.getBoundingClientRect();
                const cs = window.getComputedStyle(el);
                return {
                    top: Math.round(r.top),
                    bottom: Math.round(r.bottom),
                    left: Math.round(r.left),
                    right: Math.round(r.right),
                    width: Math.round(r.width),
                    height: Math.round(r.height),
                    position: cs.position,
                    overflow: cs.overflow,
                    overflowY: cs.overflowY,
                    display: cs.display,
                    transform: cs.transform,
                    animation: cs.animationName,
                    scrollHeight: el.scrollHeight,
                    clientHeight: el.clientHeight
                };
            }

            return {
                windowInnerHeight: window.innerHeight,
                windowInnerWidth: window.innerWidth,
                windowScrollY: window.scrollY,
                docScrollHeight: document.documentElement.scrollHeight,
                bodyScrollHeight: document.body.scrollHeight,
                btnNext: getInfo(nextBtn),
                bottomBar: getInfo(bottomBar),
                testStep4: getInfo(testStep4),
                qCard: getInfo(qCard),
                optContainer: getInfo(optContainer),
                appMain: getInfo(appMain),
                pageBody: getInfo(pageBody)
            };
        })()
        """
        metrics_res = send_cmd("Runtime.evaluate", {"expression": measure_script, "returnByValue": True})
        metrics = metrics_res.get("result", {}).get("value", {})
        print("\n--- VIEWPORT & ELEMENT METRICS ---")
        print(json.dumps(metrics, indent=2))

        # Take screenshot
        ss_res = send_cmd("Page.captureScreenshot")
        import base64
        ss_data = base64.b64decode(ss_res.get("data", ""))
        ss_path = os.path.join(ROOT, "scripts", "diagnostic_mock_test.png")
        with open(ss_path, "wb") as f:
            f.write(ss_data)
        print(f"\nScreenshot saved to: {ss_path}")

    finally:
        proc.terminate()

if __name__ == "__main__":
    run_diagnostics()
