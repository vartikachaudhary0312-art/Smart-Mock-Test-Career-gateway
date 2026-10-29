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
    admin_pw = client.application.config.get("ADMIN_PASSWORD") or "Vartika@123"
    response = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": admin_pw,
        "role": "admin"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["user"]["role"] == "admin"
    assert data["data"]["user"]["email"] == "vartikachaudhary0312@gmail.com"
    assert "token" in data["data"]

def test_admin_login_wrong_password_rejected(client):
    """Wrong admin password must be rejected with 401."""
    response = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "WrongPassword999!",
        "role": "admin"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert "Invalid email or password" in data["message"]

def test_unauthorized_email_admin_login_rejected(client):
    """Any email other than vartikachaudhary0312@gmail.com requesting admin role must get 403."""
    response = client.post("/api/auth/login", json={
        "email": "otheruser@example.com",
        "password": "Vartika@123",
        "role": "admin"
    })
    assert response.status_code == 403
    data = response.get_json()
    assert data["success"] is False
    assert "Only the designated administrator account is authorized" in data["message"]

def test_admin_credentials_in_student_login_rejected(client):
    """Attempting Admin credentials under Student login MUST be rejected with 403."""
    response = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "Vartika@123",
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
    assert "Only the designated administrator account is authorized" in data["message"]

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
    assert data["data"]["user"]["role"] == "student"

def test_public_registration_cannot_register_admin_email(client):
    """Public registration cannot register using the reserved Admin email."""
    response = client.post("/api/auth/register", json={
        "name": "Impostor Admin",
        "email": "vartikachaudhary0312@gmail.com",
        "mobile": "+91 9998887770",
        "password": "Password@123",
        "confirm_password": "Password@123"
    })
    assert response.status_code == 403
    data = response.get_json()
    assert data["success"] is False
    assert "reserved for system administration" in data["message"]

def test_public_registration_forces_student_role(client):
    """Submitting role='admin' during registration must be ignored and assigned 'student'."""
    import time
    unique_email = f"escalation_test_{int(time.time() * 1000)}@test.com"
    response = client.post("/api/auth/register", json={
        "name": "Role Escalation Attempt",
        "email": unique_email,
        "mobile": "+91 9998887770",
        "password": "Password@123",
        "confirm_password": "Password@123",
        "role": "admin"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["data"]["user"]["role"] == "student"

def test_missing_admin_password_refuses_login(client, monkeypatch):
    """When ADMIN_PASSWORD is not set or empty, Admin login must be refused with 503."""
    client.application.config["ADMIN_PASSWORD"] = ""
    monkeypatch.setenv("ADMIN_PASSWORD", "")

    response = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "Vartika@123",
        "role": "admin"
    })
    assert response.status_code == 503
    data = response.get_json()
    assert data["success"] is False
    assert "Admin password is not configured on the server" in data["message"]

def test_student_cannot_access_admin_api(client):
    """A student token must be rejected when attempting to access Admin endpoints."""
    # Obtain student token
    login_res = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "Student@123",
        "role": "student"
    })
    student_token = login_res.get_json()["data"]["token"]

    # Attempt accessing admin dashboard
    admin_res = client.get("/api/admin/dashboard", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert admin_res.status_code == 403
    data = admin_res.get_json()
    assert data["success"] is False
    assert "Access denied" in data["message"]

def test_admin_can_access_admin_api(client):
    """The configured admin token must be accepted for Admin endpoints."""
    # Restore admin password in testing config for this test
    client.application.config["ADMIN_PASSWORD"] = "Vartika@123"

    login_res = client.post("/api/auth/login", json={
        "email": "vartikachaudhary0312@gmail.com",
        "password": "Vartika@123",
        "role": "admin"
    })
    admin_token = login_res.get_json()["data"]["token"]

    admin_res = client.get("/api/admin/dashboard", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert admin_res.status_code == 200
    data = admin_res.get_json()
    assert data["success"] is True
    assert "total_students" in data["data"]
