import subprocess
import time
import json
import requests
import websocket

PORT = 9560
PROFILE = r"C:\Windows\Temp\ch_mobile_dbg"
cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    f"--remote-debugging-port={PORT}",
    "--disable-gpu",
    f"--user-data-dir={PROFILE}",
    "--window-size=375,667",
    "http://127.0.0.1:5000/login.html"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    pages = requests.get(f"http://127.0.0.1:{PORT}/json").json()
    ws = websocket.create_connection(pages[0]["webSocketDebuggerUrl"])
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

    eval_js("""
        localStorage.setItem('smt_current_user', JSON.stringify({id: 1, name: 'Rahul', role: 'student'}));
        localStorage.setItem('smt_auth_token', 'xyz');
    """)
    eval_js("window.location.href = 'http://127.0.0.1:5000/mock-test.html'")
    time.sleep(2)

    info = eval_js("""
    (async function() {
        const sub = MockTestEngine.allSubjects[0];
        MockTestEngine.selectSubject(sub);
        MockTestEngine.hasActiveCamera = () => true;
        MockTestEngine.facePresenceVerified = true;
        await MockTestEngine.startActualTest();

        const hdr = document.querySelector('.test-header-bar');
        const qCard = document.querySelector('.test-question-card');
        const metaHdr = document.querySelector('.test-question-meta-header');
        const qText = document.getElementById('testQuestionText');
        const opts = document.getElementById('testOptionsContainer');
        const bar = document.getElementById('testBottomActionBar');
        const btn = document.getElementById('btnNextQuestion');

        return {
            windowW: window.innerWidth,
            windowH: window.innerHeight,
            hdrRect: hdr ? hdr.getBoundingClientRect().toJSON() : null,
            qCardRect: qCard ? qCard.getBoundingClientRect().toJSON() : null,
            metaHdrRect: metaHdr ? metaHdr.getBoundingClientRect().toJSON() : null,
            qTextRect: qText ? qText.getBoundingClientRect().toJSON() : null,
            optsRect: opts ? opts.getBoundingClientRect().toJSON() : null,
            barRect: bar ? bar.getBoundingClientRect().toJSON() : null,
            btnRect: btn ? btn.getBoundingClientRect().toJSON() : null
        };
    })()
    """, await_promise=True)
    print("MOBILE DEBUG INFO:")
    print(json.dumps(info, indent=2))

finally:
    proc.terminate()

