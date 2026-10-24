import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["data"]["service"] == "backend"
    assert json_data["data"]["status"] == "healthy"

def test_student_login_success(client):
    response = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "Student@123",
        "role": "student"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["user"]["role"] == "student"
    assert "token" in data["data"]

def test_admin_login_success(client):
    response = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "Vartika@123",
        "role": "admin"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["user"]["role"] == "admin"

def test_admin_credentials_in_student_login_rejected(client):
    """Attempting Admin credentials under Student login MUST be rejected with 403."""
    response = client.post("/api/auth/login", json={
        "email": "admin@example.com",
        "password": "Admin@123",
        "role": "student"
    })
    assert response.status_code == 403
    data = response.get_json()
    assert data["success"] is False
    assert "Admin account detected" in data["message"]

def test_student_credentials_in_admin_login_rejected(client):
    """Attempting Student credentials under Admin login MUST be rejected with 403."""
    response = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "Student@123",
        "role": "admin"
    })
    assert response.status_code == 403
    data = response.get_json()
    assert data["success"] is False
    assert "Student account detected" in data["message"]

def test_invalid_login(client):
    response = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "WrongPassword999",
        "role": "student"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False

def test_duplicate_registration(client):
    response = client.post("/api/auth/register", json={
        "name": "Duplicate Student",
        "email": "student@example.com",
        "password": "Student@123",
        "confirm_password": "Student@123"
    })
    assert response.status_code == 409
    data = response.get_json()
    assert data["success"] is False

def test_new_student_registration(client):
    import time
    unique_email = f"newstudent_{int(time.time() * 1000)}@test.com"
    response = client.post("/api/auth/register", json={
        "name": "New Test Student",
        "email": unique_email,
        "mobile": "+91 9998887770",
        "location": "Agra, India",
        "password": "TestStudent@123",
        "confirm_password": "TestStudent@123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert "token" in data["data"]
