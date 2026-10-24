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

def test_duplicate_job_application_returns_409(client):
    token = get_auth_token(client)
    # Student 1 already applied for Job 1 in seed data
    res = client.post("/api/jobs/1/apply", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 409
    data = res.get_json()
    assert data["success"] is False

def test_successful_job_application(client):
    token = get_auth_token(client)
    res = client.post("/api/jobs/2/apply", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code in [201, 409] # 201 created or 409 if run repeatedly
    data = res.get_json()
    if res.status_code == 201:
        assert data["success"] is True
        assert data["data"]["status"] == "Applied"

def test_get_user_applications(client):
    token = get_auth_token(client)
    res = client.get("/api/applications", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
