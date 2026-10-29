import subprocess, time, json, os, requests, websocket

PORT = 9444
PROFILE = os.path.join(os.environ.get("TEMP", "."), "chrome_test_profile_diag")

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
        target = [p for p in pages if p.get("type") == "page"][0]
    ws = websocket.create_connection(target["webSocketDebuggerUrl"])

    def send_cmd(method, params=None):
        payload = {"id": 1, "method": method, "params": params or {}}
        ws.send(json.dumps(payload))
        while True:
            resp = json.loads(ws.recv())
            if resp.get("id") == 1:
                return resp.get("result", {})

    send_cmd("Runtime.evaluate", {"expression": """
        localStorage.setItem("smt_current_user", JSON.stringify({id: 1, name: "Rahul", email: "student@example.com", role: "student"}));
        localStorage.setItem("smt_auth_token", "test_tok");
    """})

    send_cmd("Page.navigate", {"url": "http://127.0.0.1:5000/mock-test.html"})
    time.sleep(1.5)

    send_cmd("Runtime.evaluate", {"expression": """
        (async function() {
            const sub = MockTestEngine.allSubjects[0];
            MockTestEngine.selectSubject(sub);
            MockTestEngine.hasActiveCamera = () => true;
            MockTestEngine.facePresenceVerified = true;
            await MockTestEngine.startActualTest();
        })()
    """, "awaitPromise": True})
    time.sleep(1)

    diag = send_cmd("Runtime.evaluate", {"expression": """
    (function() {
        const bar = document.getElementById("testBottomActionBar");
        const inner = bar ? bar.querySelector(".test-bottom-action-inner") : null;
        const left = bar ? bar.querySelector(".test-bottom-left-group") : null;
        const center = bar ? bar.querySelector(".test-bottom-center-info") : null;
        const right = bar ? bar.querySelector(".test-bottom-right-group") : null;
        const btn = document.getElementById("btnNextQuestion");

        function details(el, name) {
            if (!el) return { name, error: "null" };
            const r = el.getBoundingClientRect();
            const cs = window.getComputedStyle(el);
            return {
                name,
                rect: { top: r.top, bottom: r.bottom, left: r.left, right: r.right, width: r.width, height: r.height },
                display: cs.display,
                flexDirection: cs.flexDirection,
                flexWrap: cs.flexWrap,
                position: cs.position,
                boxSizing: cs.boxSizing,
                offsetParent: el.offsetParent ? el.offsetParent.tagName + "." + el.offsetParent.className : null
            };
        }

        return {
            windowH: window.innerHeight,
            windowW: window.innerWidth,
            bar: details(bar, "bar"),
            inner: details(inner, "inner"),
            left: details(left, "left"),
            center: details(center, "center"),
            right: details(right, "right"),
            btn: details(btn, "btn")
        };
    })()
    """, "returnByValue": True})

    print(json.dumps(diag["result"]["value"], indent=2))

finally:
    proc.terminate()
