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

def post_multipart(url, token, filename, file_bytes):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
    body.extend(b"Content-Type: application/pdf\r\n\r\n")
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(url, data=bytes(body), method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))

def run():
    print("=" * 65)
    print("  VERIFYING RESUME ANALYSIS & NAVBAR COMPONENT INTEGRATION")
    print("=" * 65)

    # 1. Verify resume.html is served via Flask
    with urllib.request.urlopen(f"{BASE_URL}/resume.html", timeout=5) as resp:
        html = resp.read().decode("utf-8")
        assert resp.getcode() == 200
        assert "resumeUploadView" in html
        assert "Resume Analysis" in html
        assert "resumeDropzone" in html
        print("[+] 1. GET /resume.html served successfully via Flask (200 OK)")

    # 2. Login to get token
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
        print(f"[+] 2. Student logged in. Token acquired: {token[:15]}...")

    # 3. Live multipart file upload to /api/resume/upload
    fake_pdf = b"%PDF-1.4 Mock resume file for live socket testing"
    code, res = post_multipart(f"{BASE_URL}/api/resume/upload", token, "Live_Candidate_Resume.pdf", fake_pdf)
    assert code == 200
    assert res["success"] is True
    analysis = res["data"]
    assert analysis["fileName"] == "Live_Candidate_Resume.pdf"
    assert "matchScore" in analysis
    assert len(analysis["parsedSkills"]) > 0
    print(f"[+] 3. Live POST /api/resume/upload returned 200 OK")
    print(f"       - Extracted Skills: {analysis['parsedSkills'][:4]}...")
    print(f"       - ATS Match Score: {analysis['matchScore']}%")
    print(f"       - Qualification: {analysis['education']}")

    # 4. Live GET /api/resume/latest
    req = urllib.request.Request(f"{BASE_URL}/api/resume/latest", method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=5) as resp:
        code = resp.getcode()
        latest = json.loads(resp.read().decode("utf-8"))["data"]
        assert code == 200
        assert latest["fileName"] == "Live_Candidate_Resume.pdf"
        print(f"[+] 4. Live GET /api/resume/latest returned saved profile: {latest['fileName']}")

    print("\n" + "=" * 65)
    print("  ALL RESUME ANALYSIS VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run()

