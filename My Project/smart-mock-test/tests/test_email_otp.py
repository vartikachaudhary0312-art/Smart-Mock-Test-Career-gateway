import re
import uuid

import pytest

from backend.app import create_app
from backend.services.email_otp_service import EmailOTPService


@pytest.fixture
def client(monkeypatch):
    app = create_app("testing")
    app.config.update({
        "MAIL_SERVER": "smtp.example.test",
        "MAIL_PORT": 587,
        "MAIL_USE_TLS": True,
        "MAIL_USE_SSL": False,
        "MAIL_USERNAME": "sender@example.test",
        "MAIL_PASSWORD": "test-password",
        "MAIL_DEFAULT_SENDER": "sender@example.test",
        "OTP_TTL_SECONDS": 300,
        "OTP_RESEND_COOLDOWN_SECONDS": 0
    })
    with app.test_client() as test_client:
        yield test_client


def test_test_otp_send_and_verify(client, monkeypatch):
    delivered = []

    def capture_email(self, config, email, code, ttl_seconds):
        delivered.append({"email": email, "code": code, "ttl": ttl_seconds})

    monkeypatch.setattr(EmailOTPService, "_deliver_email", capture_email)
    email = f"student-{uuid.uuid4().hex}@example.test"

    send_response = client.post("/api/auth/test-otp/send", json={"email": email})
    assert send_response.status_code == 200
    assert send_response.get_json()["data"]["email_masked"].endswith("@example.test")
    assert re.fullmatch(r"\d{6}", delivered[0]["code"])
    assert delivered[0]["email"] == email
    assert delivered[0]["ttl"] == 300

    verify_response = client.post("/api/auth/test-otp/verify", json={
        "email": email,
        "code": delivered[0]["code"]
    })
    assert verify_response.status_code == 200
    assert verify_response.get_json()["data"]["verified"] is True

    reuse_response = client.post("/api/auth/test-otp/verify", json={
        "email": email,
        "code": delivered[0]["code"]
    })
    assert reuse_response.status_code == 400


def test_test_otp_requires_valid_email(client):
    response = client.post("/api/auth/test-otp/send", json={"email": "not-an-email"})
    assert response.status_code == 400


def test_test_otp_send_requires_smtp_configuration(client):
    client.application.config["MAIL_SERVER"] = ""
    response = client.post("/api/auth/test-otp/send", json={"email": "student@example.test"})
    assert response.status_code == 503


def test_test_otp_wrong_code_is_rejected(client, monkeypatch):
    monkeypatch.setattr("backend.services.email_otp_service.secrets.randbelow", lambda _: 1)
    monkeypatch.setattr(EmailOTPService, "_deliver_email", lambda *args: None)
    email = f"student-{uuid.uuid4().hex}@example.test"
    client.post("/api/auth/test-otp/send", json={"email": email})

    response = client.post("/api/auth/test-otp/verify", json={
        "email": email,
        "code": "000000"
    })
    assert response.status_code == 400