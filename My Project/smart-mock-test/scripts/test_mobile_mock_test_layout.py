"""
SMART MOCK TEST & CAREER GATEWAY
Mobile Viewport Verification for Mock Test Assessment
"""

import subprocess
import time
import json
import os
import requests
import websocket

PORT = 9666
PROFILE = os.path.join(os.environ.get("TEMP", "."), "chrome_test_prof_mobile")

def test_mobile_viewport(w=375, h=667):
    print(f"\n--- Testing Mobile Viewport: {w}x{h} ---")
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        f"--remote-debugging-port={PORT}",
        "--disable-gpu",
        f"--user-data-dir={PROFILE}",
        f"--window-size={w},{h}",
        "http://127.0.0.1:5000/mock-test.html"
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
                    return resp.get("result", {}).get("result", {}).get("value")

        eval_js("""
            localStorage.setItem("smt_current_user", JSON.stringify({id: 1, name: "Rahul", email: "student@example.com", role: "student"}));
            localStorage.setItem("smt_auth_token", "test_tok");
        """)
        eval_js("window.location.href = 'http://127.0.0.1:5000/mock-test.html'")
        time.sleep(1.5)

        eval_js("""
            (async function() {
                const sub = MockTestEngine.allSubjects[0];
                MockTestEngine.selectSubject(sub);
                MockTestEngine.hasActiveCamera = () => true;
                MockTestEngine.facePresenceVerified = true;
                await MockTestEngine.startActualTest();
            })()
        """, await_promise=True)
        time.sleep(1)

        m = eval_js("""
        (function() {
            const btn = document.getElementById("btnNextQuestion");
            const bar = document.getElementById("testBottomActionBar");
            const rBtn = btn.getBoundingClientRect();
            const rBar = bar.getBoundingClientRect();

            return {
                windowH: window.innerHeight,
                windowW: window.innerWidth,
                scrollY: window.scrollY,
                btnVisible: rBtn.top >= 0 && rBtn.bottom <= window.innerHeight,
                btnTop: Math.round(rBtn.top),
                btnBottom: Math.round(rBtn.bottom),
                barTop: Math.round(rBar.top),
                barBottom: Math.round(rBar.bottom)
            };
        })()
        """)
        print("  Mobile metrics:", json.dumps(m, indent=2))
        assert m["btnVisible"], f"Continue button NOT visible in mobile viewport! btnTop: {m['btnTop']}, btnBottom: {m['btnBottom']}, windowH: {m['windowH']}"
        assert m["scrollY"] == 0, f"Page scrolled on mobile! scrollY: {m['scrollY']}"
        print(f"  [PASS] Mobile viewport {w}x{h} verified: Continue button is fully visible in viewport without scrolling!")
    finally:
        proc.terminate()

if __name__ == "__main__":
    test_mobile_viewport(375, 667) # iPhone SE
    test_mobile_viewport(414, 896) # iPhone 11/XR
    test_mobile_viewport(768, 1024) # iPad

