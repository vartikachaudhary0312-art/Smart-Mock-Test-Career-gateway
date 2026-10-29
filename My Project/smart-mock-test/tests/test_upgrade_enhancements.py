import pytest
from backend.app import create_app
from backend.repositories.user_repository import UserRepository
from backend.repositories.attempt_repository import AttemptRepository
from backend.repositories.question_repository import QuestionRepository

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def test_register_and_profile_retrieval_real_user(client):
    """Verify that registering a real user (e.g. Ritesh Raushan) stores and returns their real profile data."""
    email = "ritesh.raushan.test@example.com"
    payload = {
        "name": "Ritesh Raushan",
        "email": email,
        "password": "Password@123",
        "confirm_password": "Password@123",
        "mobile": "+91 9876543219",
        "location": "Patna, India",
        "education": "B.Tech Computer Science, NIT"
    }

    # Register
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code in [201, 409]

    # Login
    login_res = client.post("/api/auth/login", json={"email": email, "password": "Password@123"})
    assert login_res.status_code == 200
    login_data = login_res.get_json()["data"]
    assert login_data["user"]["name"] == "Ritesh Raushan"
    assert login_data["user"]["email"] == email
    token = login_data["token"]

    # Verify /api/auth/me returns Ritesh Raushan, not demo user
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_user = me_res.get_json()["data"]["user"]
    assert me_user["name"] == "Ritesh Raushan"
    assert me_user["email"] == email
    assert me_user["id"] == login_data["user"]["id"]

    # Verify /api/student/profile returns Ritesh Raushan
    prof_res = client.get("/api/student/profile", headers={"Authorization": f"Bearer {token}"})
    assert prof_res.status_code == 200
    prof_data = prof_res.get_json()["data"]["profile"]
    assert prof_data["name"] == "Ritesh Raushan"
    assert prof_data["email"] == email

def test_mock_test_supports_50_questions(client):
    """Verify that starting a mock test with length=50 returns 50 questions for subjects with 50+ questions."""
    login_res = client.post("/api/auth/login", json={"email": "student@example.com", "password": "Student@123"})
    token = login_res.get_json()["data"]["token"]

    # Start test for DSA (has 100 questions) requesting 50 questions
    res = client.post("/api/tests/sub_dsa/start", headers={"Authorization": f"Bearer {token}"}, json={
        "length": 50,
        "difficulty": "medium"
    })
    assert res.status_code == 200
    data = res.get_json()["data"]
    questions = data["questions"]
    assert len(questions) == 50

    # Ensure answers and explanations are stripped
    for q in questions:
        assert "correct_option" not in q
        assert "correctIndex" not in q
        assert "explanation" not in q
        assert len(q["options"]) == 4

def test_unseen_question_prioritization_and_rotation(client):
    """Verify that subsequent mock test attempts prioritize unseen questions before repeating."""
    login_res = client.post("/api/auth/login", json={"email": "student@example.com", "password": "Student@123"})
    token = login_res.get_json()["data"]["token"]

    # Attempt 1: Request 50 questions for Java
    res1 = client.post("/api/tests/sub_java/start", headers={"Authorization": f"Bearer {token}"}, json={"length": 50})
    assert res1.status_code == 200
    attempt1_qids = set(q["id"] for q in res1.get_json()["data"]["questions"])
    assert len(attempt1_qids) == 50

    # Attempt 2: Request 25 questions for Java (Java has 75 total questions, so 25 unseen remain!)
    res2 = client.post("/api/tests/sub_java/start", headers={"Authorization": f"Bearer {token}"}, json={"length": 25})
    assert res2.status_code == 200
    attempt2_qids = set(q["id"] for q in res2.get_json()["data"]["questions"])
    assert len(attempt2_qids) == 25

    # Since 25 unseen questions were available, ALL 25 should be unseen (0 overlap with attempt 1)!
    overlap = attempt1_qids.intersection(attempt2_qids)
    assert len(overlap) == 0, f"Expected 0 overlap between attempt 1 (50 Qs) and attempt 2 (25 Qs), but found {len(overlap)}"

def test_logout_endpoint(client):
    """Verify backend logout returns 200 and success."""
    res = client.post("/api/auth/logout")
    assert res.status_code == 200
    assert res.get_json()["success"] is True

