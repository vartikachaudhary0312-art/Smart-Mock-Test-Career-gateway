import os
import sys
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app import create_app

def run_verification():
    print("=" * 70)
    print("  VERIFYING ADMIN AUTHENTICATION & SINGLE ADMIN ENFORCEMENT")
    print("=" * 70)

    app = create_app("testing")
    client = app.test_client()

    results = []

    # 1. UI Check: Demo shortcuts removed from login.html
    login_html = (PROJECT_ROOT / "frontend" / "login.html").read_text(encoding="utf-8")
    demo_in_login = any(k in login_html for k in ["btnFillStudentDemo", "btnFillAdminDemo", "QUICK DEMO CREDENTIALS"])
    results.append(("1. Demo shortcuts removed from login.html", not demo_in_login))
    assert not demo_in_login, "Demo controls still present in login.html"

    # 2. UI Check: Admin registration controls removed from register.html
    reg_html = (PROJECT_ROOT / "frontend" / "register.html").read_text(encoding="utf-8")
    admin_in_reg = any(k in reg_html for k in ["adminSecurityKeyGroup", "ADMIN2026", "data-role=\"admin\""])
    results.append(("2. Admin registration controls removed from register.html", not admin_in_reg))
    assert not admin_in_reg, "Admin controls still present in register.html"

    # 3. Successful Admin Login
    app.config["ADMIN_PASSWORD"] = "Vartika@123"
    res = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "Vartika@123",
        "role": "admin"
    })
    admin_success = res.status_code == 200 and res.get_json()["data"]["user"]["role"] == "admin"
    admin_token = res.get_json().get("data", {}).get("token")
    results.append(("3. Authorized Admin login with configured password", admin_success))
    assert admin_success, f"Admin login failed: {res.get_json()}"

    # 4. Reject Wrong Admin Password
    res = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "WrongPassword999!",
        "role": "admin"
    })
    wrong_pw = res.status_code == 401
    results.append(("4. Reject wrong Admin password with 401", wrong_pw))
    assert wrong_pw, f"Wrong password check failed: {res.status_code}"

    # 5. Reject Other Email from Admin Login
    res = client.post("/api/auth/login", json={
        "email": "impostor@example.com",
        "password": "Vartika@123",
        "role": "admin"
    })
    impostor_rejected = res.status_code == 403
    results.append(("5. Reject non-admin email from Admin login with 403", impostor_rejected))
    assert impostor_rejected, f"Impostor not rejected: {res.status_code}"

    # 6. Admin Credentials under Student Login Rejected
    res = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "Vartika@123",
        "role": "student"
    })
    admin_in_student_rejected = res.status_code == 403 and "Admin account detected" in res.get_json()["message"]
    results.append(("6. Admin credentials under student tab rejected with 403", admin_in_student_rejected))
    assert admin_in_student_rejected, f"Role separation failed: {res.get_json()}"

    # 7. Student Login Works
    res = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "Student@123",
        "role": "student"
    })
    student_success = res.status_code == 200 and res.get_json()["data"]["user"]["role"] == "student"
    student_token = res.get_json().get("data", {}).get("token")
    results.append(("7. Legitimate Student login succeeds with 200", student_success))
    assert student_success, f"Student login failed: {res.get_json()}"

    # 8. Student Token Accessing Admin Endpoint Rejected
    res = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {student_token}"})
    student_blocked_from_admin = res.status_code == 403
    results.append(("8. Student token accessing /api/admin/dashboard blocked with 403", student_blocked_from_admin))
    assert student_blocked_from_admin, f"Student should be blocked from admin API: {res.status_code}"

    # 9. Admin Token Accessing Admin Endpoint Authorized
    res = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {admin_token}"})
    admin_allowed = res.status_code == 200
    results.append(("9. Admin token accessing /api/admin/dashboard authorized with 200", admin_allowed))
    assert admin_allowed, f"Admin was blocked from admin API: {res.status_code}"

    # 10. Public Registration Cannot Register Reserved Admin Email
    res = client.post("/api/auth/register", json={
        "name": "Admin Hijacker",
        "email": "vartikachaudhary0312@gmail.com",
        "password": "Password@123",
        "confirm_password": "Password@123"
    })
    admin_reg_blocked = res.status_code == 403
    results.append(("10. Registration with Admin email rejected with 403", admin_reg_blocked))
    assert admin_reg_blocked, f"Registration with Admin email should be rejected: {res.status_code}"

    # 11. Registration Forces Student Role
    import time
    t_email = f"student_check_{int(time.time() * 1000)}@college.edu"
    res = client.post("/api/auth/register", json={
        "name": "Student Role Check",
        "email": t_email,
        "password": "Password@123",
        "confirm_password": "Password@123",
        "role": "admin"
    })
    role_forced_student = res.status_code == 201 and res.get_json()["data"]["user"]["role"] == "student"
    results.append(("11. Public registration payload with role='admin' forced to 'student'", role_forced_student))
    assert role_forced_student, f"Registration role forcing failed: {res.get_json()}"

    # 12. Missing ADMIN_PASSWORD Refuses Admin Login with 503
    app.config["ADMIN_PASSWORD"] = ""
    os.environ["ADMIN_PASSWORD"] = ""
    res = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "Vartika@123",
        "role": "admin"
    })
    missing_pw_refused = res.status_code == 503 and "Admin password is not configured" in res.get_json()["message"]
    results.append(("12. Missing ADMIN_PASSWORD refuses Admin login with 503", missing_pw_refused))
    assert missing_pw_refused, f"Missing ADMIN_PASSWORD should return 503: {res.status_code}"

    print("\nVerification Test Results Summary:")
    print("-" * 70)
    for name, ok in results:
        status = "PASSED" if ok else "FAILED"
        print(f"  [{status}] {name}")
    print("-" * 70)
    print(f"Total: {len(results)} / {len(results)} checks PASSED successfully!\n")

if __name__ == "__main__":
    run_verification()

