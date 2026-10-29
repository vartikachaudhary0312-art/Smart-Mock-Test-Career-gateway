import os
import sys
import time
import subprocess
import json
import urllib.request
import urllib.error
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

BASE_URL = "http://127.0.0.1:5000"

def http_req(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            try:
                parsed = json.loads(body)
            except Exception:
                parsed = body
            return status, parsed
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = body
        return status, parsed

def run_live_tests():
    print("=" * 70)
    print("  LIVE HTTP SOCKET & AUTHENTICATION INTEGRATION SUITE")
    print("=" * 70)

    # 1. Start server process
    run_py = str(PROJECT_ROOT / "run.py")
    server_proc = subprocess.Popen(
        [sys.executable, run_py],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(PROJECT_ROOT)
    )

    try:
        # Wait for server to bind to port 5000
        print("\n[+] Booting server on http://127.0.0.1:5000...")
        max_retries = 20
        healthy = False
        for attempt in range(max_retries):
            try:
                status, res = http_req(f"{BASE_URL}/api/health")
                if status == 200:
                    healthy = True
                    print(f"    Server online! Status: {res.get('data', {}).get('status')}")
                    break
            except Exception:
                time.sleep(0.5)

        assert healthy, "Server failed to start within timeout"

        # 2. Test Static Frontend Page Delivery
        print("\n[+] Testing static page delivery over unified Flask origin...")
        status, html = http_req(f"{BASE_URL}/login.html")
        assert status == 200 and "loginForm" in html, "Failed to serve login.html"
        print("    [PASSED] GET /login.html served correctly (200 OK)")

        status, html = http_req(f"{BASE_URL}/register.html")
        assert status == 200 and "registerForm" in html, "Failed to serve register.html"
        print("    [PASSED] GET /register.html served correctly (200 OK)")

        status, html = http_req(f"{BASE_URL}/admin/dashboard.html")
        assert status == 200 and "adminDashboardView" in html, "Failed to serve admin/dashboard.html"
        print("    [PASSED] GET /admin/dashboard.html served correctly (200 OK)")

        # 3. Test Admin Authentication with Live Credentials
        print("\n[+] Testing Admin Authentication...")
        admin_email = "vartikachaudhary0312@gmail.com"
        admin_pw = "Vartika1234@#"

        # Wrong password rejection
        status, res = http_req(f"{BASE_URL}/api/auth/login", method="POST", data={
            "email": admin_email,
            "password": "WrongAdminPassword!",
            "role": "admin"
        })
        assert status == 401, f"Expected 401 on wrong admin password, got {status}"
        print("    [PASSED] Wrong Admin password rejected with HTTP 401")

        # Impostor admin email rejection
        status, res = http_req(f"{BASE_URL}/api/auth/login", method="POST", data={
            "email": "hacker@example.com",
            "password": admin_pw,
            "role": "admin"
        })
        assert status == 403, f"Expected 403 on impostor admin, got {status}"
        print("    [PASSED] Impostor Admin email rejected with HTTP 403")

        # Legitimate Admin login
        status, res = http_req(f"{BASE_URL}/api/auth/login", method="POST", data={
            "email": admin_email,
            "password": admin_pw,
            "role": "admin"
        })
        assert status == 200 and res.get("success") is True, f"Admin login failed: {res}"
        admin_token = res["data"]["token"]
        assert res["data"]["user"]["role"] == "admin"
        print(f"    [PASSED] Authorized Admin login succeeded (HTTP 200), Token: {admin_token[:20]}...")

        # Admin accessing protected admin endpoints
        status, res = http_req(f"{BASE_URL}/api/admin/dashboard", headers={"Authorization": f"Bearer {admin_token}"})
        assert status == 200 and "total_students" in res.get("data", {}), f"Admin dashboard failed: {res}"
        print(f"    [PASSED] Admin GET /api/admin/dashboard -> total_students={res['data']['total_students']}")

        # 4. Test Student Registration & Authentication
        print("\n[+] Testing Student Registration & Role Isolation...")
        test_email = f"live_student_{int(time.time())}@example.com"
        status, res = http_req(f"{BASE_URL}/api/auth/register", method="POST", data={
            "name": "Ritesh Raushan",
            "email": test_email,
            "mobile": "+91 9876543210",
            "location": "Patna, Bihar",
            "password": "StudentLive@123",
            "confirm_password": "StudentLive@123"
        })
        assert status == 201 and res.get("success") is True, f"Student registration failed: {res}"
        student_id = res["data"]["user"]["id"]
        student_token = res["data"]["token"]
        print(f"    [PASSED] Student registration created ID #{student_id} (HTTP 201)")

        # Verify Student cannot access Admin API
        status, res = http_req(f"{BASE_URL}/api/admin/dashboard", headers={"Authorization": f"Bearer {student_token}"})
        assert status == 403, f"Expected 403 for student accessing admin API, got {status}"
        print("    [PASSED] Student token forbidden from Admin dashboard (HTTP 403)")

        # Verify Student can access their own profile
        status, res = http_req(f"{BASE_URL}/api/student/profile", headers={"Authorization": f"Bearer {student_token}"})
        assert status == 200 and res["data"]["profile"]["name"] == "Ritesh Raushan", f"Profile retrieval failed: {res}"
        print(f"    [PASSED] Student GET /api/student/profile returned name '{res['data']['profile']['name']}'")

        # 5. Test Live Admin Student Management & Suspension Flow
        print("\n[+] Testing Live Admin Student Management & Suspension...")
        # Admin gets student list and sees new student
        status, res = http_req(f"{BASE_URL}/api/admin/students", headers={"Authorization": f"Bearer {admin_token}"})
        assert status == 200
        found_student = next((s for s in res["data"] if s["id"] == student_id), None)
        assert found_student is not None, f"Newly registered student #{student_id} not found in admin students"
        print(f"    [PASSED] Admin located student #{student_id} in GET /api/admin/students")

        # Admin blocks student
        status, res = http_req(
            f"{BASE_URL}/api/admin/students/{student_id}/status",
            method="PUT",
            data={"status": "Blocked"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert status == 200 and res["data"]["status"] == "Blocked"
        print(f"    [PASSED] Admin updated student #{student_id} status to 'Blocked'")

        # Blocked student attempts login
        status, res = http_req(f"{BASE_URL}/api/auth/login", method="POST", data={
            "email": test_email,
            "password": "StudentLive@123",
            "role": "student"
        })
        assert status == 403 and "suspended" in res.get("message", "").lower(), f"Expected suspended 403, got {status}: {res}"
        print("    [PASSED] Blocked student login rejected with HTTP 403 (Account suspended)")

        # Admin reactivates student
        status, res = http_req(
            f"{BASE_URL}/api/admin/students/{student_id}/status",
            method="PUT",
            data={"status": "Active"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert status == 200 and res["data"]["status"] == "Active"
        print(f"    [PASSED] Admin reactivated student #{student_id} to 'Active'")

        # Student logs in successfully again
        status, res = http_req(f"{BASE_URL}/api/auth/login", method="POST", data={
            "email": test_email,
            "password": "StudentLive@123",
            "role": "student"
        })
        assert status == 200 and res.get("success") is True
        print(f"    [PASSED] Reactivated student logged in successfully (HTTP 200)")

        print("\n" + "=" * 70)
        print("  🎉 ALL LIVE INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
        print("=" * 70)

    finally:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=3)
        except Exception:
            server_proc.kill()

if __name__ == "__main__":
    run_live_tests()

