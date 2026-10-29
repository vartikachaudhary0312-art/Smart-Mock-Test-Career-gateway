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

def test_get_all_subjects_catalog(client):
    res = client.get("/api/subjects")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    subjects = data["data"]
    assert len(subjects) >= 86

    # Verify key categories exist
    categories = set(s.get("category_id") or s.get("category") for s in subjects)
    for cat in ["cat_quant", "cat_core_cs", "cat_programming", "cat_web_dev", "cat_db_net", "cat_company"]:
        assert cat in categories or any(cat in str(c).lower() for c in categories)

def test_get_categories_portal(client):
    res = client.get("/api/subjects/categories")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    categories = data["data"]
    assert len(categories) == 14

    names = [c["name"] for c in categories]
    assert "Quantitative Aptitude" in names
    assert "Data Interpretation" in names
    assert "Verbal Ability" in names
    assert "Logical Reasoning" in names
    assert "Verbal Reasoning" in names
    assert "Non-Verbal Reasoning" in names
    assert "Programming Tests" in names
    assert "Core Computer Science" in names
    assert "Technical MCQs" in names
    assert "Web Development & Technologies" in names
    assert "Database & Networking" in names
    assert "Company-Wise Placement Tests" in names
    assert "Technical Interview Preparation" in names
    assert "HR Interview & Communication" in names

def test_get_single_category_detail(client):
    res = client.get("/api/subjects/categories/cat_quant")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    cat = data["data"]
    assert cat["name"] == "Quantitative Aptitude"
    assert "topics" in cat
    assert len(cat["topics"]) >= 5

def test_get_single_subject_detail(client):
    res = client.get("/api/subjects/sub_prog_fund")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == "Programming Fundamentals"
    assert "topics" in data["data"]
    assert len(data["data"]["topics"]) > 0

def test_get_practice_questions_endpoint(client):
    res = client.get("/api/tests/sub_percentages/practice?difficulty=Easy&length=5")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    questions = data["data"]
    assert len(questions) > 0
    # Practice mode questions MUST include explanation and correct_option for instant feedback!
    for q in questions:
        assert "explanation" in q
        assert "correct_option" in q

def test_start_subject_mock_test_string_id(client):
    token = get_auth_token(client)
    res = client.post(
        "/api/tests/sub_prog_fund/start",
        headers={"Authorization": f"Bearer {token}"},
        json={"difficulty": "Easy", "length": 10}
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "attempt_id" in data["data"]
    assert "questions" in data["data"]
    questions = data["data"]["questions"]
    assert len(questions) > 0
    # Questions should not contain answer keys before submission in timed test mode
    for q in questions:
        assert "correct_option" not in q
        assert "correctIndex" not in q

def test_start_company_mock_test(client):
    token = get_auth_token(client)
    res = client.post(
        "/api/tests/sub_tcs/start",
        headers={"Authorization": f"Bearer {token}"},
        json={"difficulty": "Mixed", "length": 5}
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["data"]["questions"]) > 0

def test_empty_subject_returns_clean_coming_soon(client):
    token = get_auth_token(client)
    # sub_distributed has 0 questions
    res = client.post(
        "/api/tests/sub_distributed/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    data = res.get_json()
    assert data["success"] is False
    assert "Questions coming soon" in data["message"]

def test_submit_subject_mock_test(client):
    token = get_auth_token(client)
    # Start test first to get attempt_id
    start_res = client.post(
        "/api/tests/sub_prog_fund/start",
        headers={"Authorization": f"Bearer {token}"},
        json={"difficulty": "Easy", "length": 5}
    )
    assert start_res.status_code == 200
    start_data = start_res.get_json()["data"]
    attempt_id = start_data["attempt_id"]
    test_questions = start_data["questions"]

    # Submit answers
    answers = [{"question_id": q["id"], "selected_option": "A"} for q in test_questions]
    submit_res = client.post(
        "/api/tests/sub_prog_fund/submit",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "attempt_id": attempt_id,
            "answers": answers,
            "time_taken": 300
        }
    )
    assert submit_res.status_code == 200
    submit_data = submit_res.get_json()["data"]
    assert submit_data["attempt_id"] == attempt_id
    assert "score" in submit_data
    assert "percentage" in submit_data
    assert submit_data["total_questions"] == len(test_questions)
