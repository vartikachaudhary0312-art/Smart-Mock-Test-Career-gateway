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

def test_get_user_results(client):
    token = get_auth_token(client)
    res = client.get("/api/results", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)

def test_get_result_analysis(client):
    token = get_auth_token(client)
    res = client.get("/api/results/101/analysis", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    analysis = data["data"]
    assert "strong_areas" in analysis
    assert "weak_areas" in analysis
    assert "recommendations" in analysis
