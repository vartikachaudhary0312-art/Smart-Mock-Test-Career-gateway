import io
import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client

def get_auth_token(client):
    login_res = client.post("/api/auth/login", json={
        "email": "student@example.com",
        "password": "Student@123",
        "role": "student"
    })
    assert login_res.status_code == 200
    return login_res.get_json()["data"]["token"]

def test_resume_upload_success(client):
    token = get_auth_token(client)
    fake_pdf = (io.BytesIO(b"%PDF-1.4 Mock resume content for testing"), "Rahul_Sharma_Resume.pdf")

    response = client.post(
        "/api/resume/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={"file": fake_pdf},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "matchScore" in data["data"] or "match_score" in data["data"]
    assert "parsedSkills" in data["data"] or "skills" in data["data"]

def test_resume_upload_docx_success(client):
    token = get_auth_token(client)
    fake_docx = (io.BytesIO(b"PK\x03\x04 Mock docx content"), "Ritesh_Raushan_Resume.docx")

    response = client.post(
        "/api/resume/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={"file": fake_docx},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True

def test_resume_upload_invalid_extension_rejected(client):
    token = get_auth_token(client)
    fake_exe = (io.BytesIO(b"MZ executable"), "malicious_file.exe")

    response = client.post(
        "/api/resume/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={"file": fake_exe},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Invalid file format" in data["message"]

def test_resume_upload_missing_file_rejected(client):
    token = get_auth_token(client)

    response = client.post(
        "/api/resume/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

def test_get_latest_resume(client):
    token = get_auth_token(client)

    # Upload first
    fake_pdf = (io.BytesIO(b"%PDF-1.4 Mock resume"), "Test_Student_Resume.pdf")
    client.post(
        "/api/resume/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={"file": fake_pdf},
        content_type="multipart/form-data"
    )

    # Retrieve latest
    response = client.get("/api/resume/latest", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["fileName"] == "Test_Student_Resume.pdf" or data["data"]["file_name"] == "Test_Student_Resume.pdf"

