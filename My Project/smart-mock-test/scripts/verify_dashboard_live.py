import os
import sys
import json
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

BASE_URL = "http://127.0.0.1:5000"

def run():
    print("=" * 65)
    print("  VERIFYING LIVE DASHBOARD APIS & FRONTEND INTEGRATION")
    print("=" * 65)

    # 1. Check static page delivery
    with urllib.request.urlopen(f"{BASE_URL}/student-dashboard.html", timeout=5) as resp:
        assert resp.getcode() == 200
        html = resp.read().decode("utf-8")
        assert "statTestsTaken" in html
        assert "statAvgScore" in html
        assert "statBestScore" in html
        assert "statApplications" in html
        assert "recommendedJobsContainer" in html
        print("[+] 1. GET /student-dashboard.html delivered with all required stat cards (200 OK)")

    # 2. Login to get student auth token
    login_data = json.dumps({
        "email": "student@example.com",
        "password": "Student@123",
        "role": "student"
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/api/auth/login", data=login_data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        token = data["data"]["token"]
        user_id = data["data"]["user"]["id"]
        print(f"[+] 2. Student logged in (User ID #{user_id}). Token acquired.")

    # 3. Verify /api/results
    req = urllib.request.Request(f"{BASE_URL}/api/results", method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.getcode() == 200
        res = json.loads(resp.read().decode("utf-8"))
        results = res.get("data", [])
        print(f"[+] 3. GET /api/results returned {len(results)} test attempts for student #{user_id}")
        if len(results) > 0:
            r0 = results[0]
            print(f"       - Sample: subject='{r0.get('subject')}', percentage={r0.get('percentage')}%")

    # 4. Verify /api/jobs
    with urllib.request.urlopen(f"{BASE_URL}/api/jobs", timeout=5) as resp:
        assert resp.getcode() == 200
        jobs = json.loads(resp.read().decode("utf-8")).get("data", [])
        assert len(jobs) > 0
        print(f"[+] 4. GET /api/jobs returned {len(jobs)} active job postings for recommendations")
        print(f"       - Sample: title='{jobs[0].get('title')}', company='{jobs[0].get('company')}'")

    # 5. Verify /api/applications
    req = urllib.request.Request(f"{BASE_URL}/api/applications", method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.getcode() == 200
        apps = json.loads(resp.read().decode("utf-8")).get("data", [])
        print(f"[+] 5. GET /api/applications returned {len(apps)} candidate applications")

    # 6. Verify /api/student/profile
    req = urllib.request.Request(f"{BASE_URL}/api/student/profile", method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.getcode() == 200
        p = json.loads(resp.read().decode("utf-8")).get("data", {}).get("profile", {})
        print(f"[+] 6. GET /api/student/profile returned profile: {p.get('name')} ({p.get('email')})")

    print("\n" + "=" * 65)
    print("  ALL DASHBOARD LIVE INTEGRATIONS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run()

