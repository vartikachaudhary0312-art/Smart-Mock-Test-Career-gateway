import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def get_auth_token(client):
    res = client.post("/api/auth/login", json={"email": "student@example.com", "password": "Student@123"})
    return res.get_json()["data"]["token"]

def test_get_tests_list(client):
    res = client.get("/api/tests")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["data"]) > 0

def test_start_test_hides_correct_answers(client):
    token = get_auth_token(client)
    res = client.post("/api/tests/1/start", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "questions" in data["data"]
    
    questions = data["data"]["questions"]
    for q in questions:
        assert "correct_option" not in q
        assert "correctIndex" not in q

def test_submit_test_calculates_score_server_side(client):
    token = get_auth_token(client)
    res = client.post("/api/tests/1/submit", headers={"Authorization": f"Bearer {token}"}, json={
        "answers": [
            {"question_id": 1, "selected_option": "B"},
            {"question_id": 2, "selected_option": "C"}
        ],
        "time_taken": 1200
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    result = data["data"]
    assert "score" in result
    assert "percentage" in result
    assert "accuracy" in result
