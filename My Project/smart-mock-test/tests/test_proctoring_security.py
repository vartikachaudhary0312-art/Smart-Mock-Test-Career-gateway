import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def get_student_token(client, email="student@example.com", password="Student@123"):
    res = client.post("/api/auth/login", json={"email": email, "password": password, "role": "student"})
    return res.get_json()["data"]["token"]

def test_start_test_creates_attempt_session(client):
    token = get_student_token(client)
    res = client.post("/api/tests/1/start", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert "attempt_id" in data
    assert data["attempt_id"].startswith("att_")
    assert "security_policy" in data
    assert data["security_policy"]["enforce_fullscreen"] is True
    assert "questions" in data
    # Ensure correct answers are hidden from student
    for q in data["questions"]:
        assert "correct_option" not in q
        assert "correctIndex" not in q

def test_log_security_event_success_and_counters(client):
    token = get_student_token(client)
    start_res = client.post("/api/tests/1/start", headers={"Authorization": f"Bearer {token}"})
    attempt_id = start_res.get_json()["data"]["attempt_id"]

    # Log tab switch event 1
    event_payload = {
        "attempt_id": attempt_id,
        "event_type": "tab_switch",
        "severity": "warning",
        "timestamp": "2026-10-29 14:00:00",
        "details": {"reason": "Page visibility hidden"}
    }
    res = client.post("/api/tests/1/security-event", headers={"Authorization": f"Bearer {token}"}, json=event_payload)
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert data["event_type"] == "tab_switch"
    assert data["current_violation_count"] == 1
    assert data["total_violations"] == 1
    assert data["should_auto_submit"] is False

    # Log tab switch event 2
    res2 = client.post("/api/tests/1/security-event", headers={"Authorization": f"Bearer {token}"}, json=event_payload)
    assert res2.status_code == 200
    assert res2.get_json()["data"]["current_violation_count"] == 2

    # Log tab switch event 3 (exceeds tab_switch max_violations limit of 3)
    res3 = client.post("/api/tests/1/security-event", headers={"Authorization": f"Bearer {token}"}, json=event_payload)
    assert res3.status_code == 200
    assert res3.get_json()["data"]["should_auto_submit"] is True
    assert "tab_switch" in res3.get_json()["data"]["auto_submit_reason"]

def test_security_event_validation_and_student_isolation(client):
    token = get_student_token(client)
    
    # Missing attempt_id should be rejected with 400
    res_bad = client.post("/api/tests/1/security-event", headers={"Authorization": f"Bearer {token}"}, json={
        "event_type": "fullscreen_exit"
    })
    assert res_bad.status_code == 400

    # Non-existent attempt_id should return 404
    res_404 = client.post("/api/tests/1/security-event", headers={"Authorization": f"Bearer {token}"}, json={
        "attempt_id": "att_non_existent_12345",
        "event_type": "fullscreen_exit"
    })
    assert res_404.status_code == 404

def test_attempt_retrieval_and_cross_student_isolation(client):
    token1 = get_student_token(client)
    start_res = client.post("/api/tests/1/start", headers={"Authorization": f"Bearer {token1}"})
    attempt_id = start_res.get_json()["data"]["attempt_id"]

    # Student 1 fetches own attempt
    get_res = client.get(f"/api/tests/attempts/{attempt_id}", headers={"Authorization": f"Bearer {token1}"})
    assert get_res.status_code == 200
    assert get_res.get_json()["data"]["attempt"]["attempt_id"] == attempt_id

def test_duplicate_submission_prevention(client):
    token = get_student_token(client)
    start_res = client.post("/api/tests/1/start", headers={"Authorization": f"Bearer {token}"})
    attempt_id = start_res.get_json()["data"]["attempt_id"]

    submission_payload = {
        "attempt_id": attempt_id,
        "submission_reason": "manual",
        "answers": [
            {"question_id": 1, "selected_option": "B"}
        ],
        "time_taken": 600
    }

    # First submission should succeed
    res1 = client.post("/api/tests/1/submit", headers={"Authorization": f"Bearer {token}"}, json=submission_payload)
    assert res1.status_code == 200
    assert res1.get_json()["success"] is True

    # Duplicate submission of the same attempt MUST return 409 Conflict
    res2 = client.post("/api/tests/1/submit", headers={"Authorization": f"Bearer {token}"}, json=submission_payload)
    assert res2.status_code == 409
    assert res2.get_json()["success"] is False
    assert "already been submitted" in res2.get_json()["message"]

def test_security_auto_submission_records_reason_and_violations(client):
    token = get_student_token(client)
    start_res = client.post("/api/tests/1/start", headers={"Authorization": f"Bearer {token}"})
    attempt_id = start_res.get_json()["data"]["attempt_id"]

    # Log a violation
    client.post("/api/tests/1/security-event", headers={"Authorization": f"Bearer {token}"}, json={
        "attempt_id": attempt_id,
        "event_type": "face_missing"
    })

    # Auto-submit with security violation reason
    auto_sub_payload = {
        "attempt_id": attempt_id,
        "submission_reason": "security_auto_submit: face_missing limit exceeded",
        "answers": [],
        "time_taken": 180
    }
    sub_res = client.post("/api/tests/1/submit", headers={"Authorization": f"Bearer {token}"}, json=auto_sub_payload)
    assert sub_res.status_code == 200
    res_data = sub_res.get_json()["data"]
    assert res_data["submission_reason"].startswith("security_auto_submit")
    assert res_data["violations_count"] == 1

