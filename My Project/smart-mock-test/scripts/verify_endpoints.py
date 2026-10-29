"""
End-to-End API Verification Script
Tests all categories, subjects, question retrieval, practice mode, and start test
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

def verify():
    app = create_app("testing")
    client = app.test_client()

    print("--- 1. Testing GET /api/subjects/categories ---")
    res = client.get("/api/subjects/categories")
    assert res.status_code == 200
    cats = res.get_json()["data"]
    print(f"Categories returned: {len(cats)}")
    assert len(cats) == 14

    print("--- 2. Testing GET /api/subjects ---")
    res = client.get("/api/subjects")
    assert res.status_code == 200
    subs = res.get_json()["data"]
    print(f"Subjects returned: {len(subs)}")
    assert len(subs) >= 86

    print("--- 3. Testing Question Counts for Major Subjects ---")
    for sid in ["sub_dsa", "sub_dbms", "sub_os", "sub_cn", "sub_oop", "sub_se", "sub_sql", "sub_c", "sub_cpp", "sub_java", "sub_python", "sub_js"]:
        res = client.get(f"/api/subjects/{sid}")
        assert res.status_code == 200
        sub_data = res.get_json()["data"]
        qcount = sub_data.get("question_count", 0)
        print(f"  {sub_data['name']} ({sid}): {qcount} questions")
        assert qcount >= 75

    print("--- 4. Testing GET /api/tests/sub_dsa/practice ---")
    res = client.get("/api/tests/sub_dsa/practice?length=5")
    assert res.status_code == 200
    p_qs = res.get_json()["data"]
    print(f"Practice questions returned: {len(p_qs)}")
    assert len(p_qs) == 5
    for q in p_qs:
        assert "explanation" in q
        assert "correct_option" in q
        assert len(q["explanation"]) > 10

    print("--- 5. Testing Student Login & Mock Test Session ---")
    login_res = client.post("/api/auth/login", json={"email": "student@example.com", "password": "Student@123"})
    assert login_res.status_code == 200
    token = login_res.get_json()["data"]["token"]

    start_res = client.post(
        "/api/tests/sub_java/start",
        headers={"Authorization": f"Bearer {token}"},
        json={"difficulty": "Medium", "length": 10}
    )
    assert start_res.status_code == 200
    start_data = start_res.get_json()["data"]
    attempt_id = start_data["attempt_id"]
    test_qs = start_data["questions"]
    print(f"Mock test started! Attempt ID: {attempt_id}, Questions: {len(test_qs)}")
    assert len(test_qs) == 10
    # Answers hidden before submission
    for q in test_qs:
        assert "correct_option" not in q

    print("--- 6. Testing Test Submission ---")
    submit_res = client.post(
        "/api/tests/sub_java/submit",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "attempt_id": attempt_id,
            "answers": [{"question_id": q["id"], "selected_option": "A"} for q in test_qs],
            "time_taken": 300,
            "violations_count": 0
        }
    )
    assert submit_res.status_code == 200
    res_data = submit_res.get_json()["data"]
    print(f"Test submitted successfully! Score: {res_data.get('score')}, Pct: {res_data.get('percentage')}%")

    print("\nALL END-TO-END VERIFICATION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    verify()
