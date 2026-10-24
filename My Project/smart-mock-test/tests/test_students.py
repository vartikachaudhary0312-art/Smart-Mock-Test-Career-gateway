import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def get_auth_token(client, email="student@example.com", password="Student@123"):
    res = client.post("/api/auth/login", json={"email": email, "password": password})
    return res.get_json()["data"]["token"]

def test_student_profile_get(client):
    token = get_auth_token(client)
    res = client.get("/api/student/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "profile" in data["data"]
    assert "password_hash" not in data["data"]["profile"]

def test_student_profile_update(client):
    token = get_auth_token(client)
    res = client.put("/api/student/profile", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "Rahul Sharma (Updated)",
        "location": "Agra, India"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["profile"]["name"] == "Rahul Sharma (Updated)"

def test_student_forbidden_admin_access(client):
    token = get_auth_token(client, "student@example.com", "Student@123")
    res = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403
    data = res.get_json()
    assert data["success"] is False
