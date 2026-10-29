import subprocess
import time
import json
import os
import requests
import websocket

PORT = 9557
PROFILE = os.path.join(os.environ.get("TEMP", "."), "chrome_inspect_steps")

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
    target = [p for p in pages if "mock-test.html" in p.get("url", "") or "login.html" in p.get("url", "")][0]
    ws = websocket.create_connection(target["webSocketDebuggerUrl"])
    msg_id = 1

    def eval_js(code, await_promise=False):
        global msg_id
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
                    print("JS Error:", res["exceptionDetails"])
                return res.get("result", {}).get("value")

    # Set auth
    eval_js("""
        localStorage.setItem("smt_current_user", JSON.stringify({id: 1, name: "Rahul Sharma", email: "student@example.com", role: "student"}));
        localStorage.setItem("smt_auth_token", "valid_token_xyz");
    """)
    eval_js("window.location.href = 'http://127.0.0.1:5000/mock-test.html'")
    time.sleep(2)

    info = eval_js("""
    (function() {
        const s1 = document.getElementById('testStep1');
        const s2 = document.getElementById('testStep2');
        const s3 = document.getElementById('testStep3');
        const s4 = document.getElementById('testStep4');
        return {
            url: window.location.href,
            s1_display: window.getComputedStyle(s1).display,
            s2_display: window.getComputedStyle(s2).display,
            s3_display: window.getComputedStyle(s3).display,
            s4_display: window.getComputedStyle(s4).display,
            s4_rect: s4.getBoundingClientRect().toJSON(),
            bodyHeight: document.body.scrollHeight,
            s4_top: s4.offsetTop
        };
    })()
    """)
    print("INITIAL STATE:", json.dumps(info, indent=2))

finally:
    proc.terminate()
