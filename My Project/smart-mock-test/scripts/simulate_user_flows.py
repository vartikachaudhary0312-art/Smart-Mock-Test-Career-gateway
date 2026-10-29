"""
Simulation script testing complete multi-account flows, 50-question mock tests,
question rotation, and profile isolation.
"""
import sys
import json
sys.path.insert(0, "My Project/smart-mock-test")

from backend.app import create_app

def run_simulation():
    app = create_app("testing")
    client = app.test_client()

    print("=== TEST 1: Register User 1 (Ritesh Raushan) ===")
    user1_payload = {
        "name": "Ritesh Raushan",
        "email": "ritesh.raushan.sim@example.com",
        "password": "Password@123",
        "confirm_password": "Password@123",
        "mobile": "+91 9123456789",
        "location": "Patna, India",
        "education": "B.Tech CSE"
    }
    r1 = client.post("/api/auth/register", json=user1_payload)
    assert r1.status_code in [201, 409], f"Register failed: {r1.get_json()}"

    l1 = client.post("/api/auth/login", json={"email": user1_payload["email"], "password": user1_payload["password"]})
    assert l1.status_code == 200
    token1 = l1.get_json()["data"]["token"]
    u1 = l1.get_json()["data"]["user"]
    assert u1["name"] == "Ritesh Raushan", f"Expected Ritesh Raushan, got {u1['name']}"
    assert u1["email"] == user1_payload["email"]
    print(f"  User 1 registered and logged in: ID={u1['id']}, Name='{u1['name']}'")

    print("\n=== TEST 2: Verify Profile API returns Ritesh Raushan ===")
    prof1 = client.get("/api/student/profile", headers={"Authorization": f"Bearer {token1}"})
    assert prof1.status_code == 200
    p1_data = prof1.get_json()["data"]["profile"]
    assert p1_data["name"] == "Ritesh Raushan"
    assert p1_data["email"] == user1_payload["email"]
    print(f"  Profile verified for User 1: Name='{p1_data['name']}', Location='{p1_data['location']}'")

    print("\n=== TEST 3: User 1 starts 50-question Mock Test (DSA) ===")
    test_res1 = client.post("/api/tests/sub_dsa/start", headers={"Authorization": f"Bearer {token1}"}, json={
        "length": 50,
        "difficulty": "medium"
    })
    assert test_res1.status_code == 200
    t1_data = test_res1.get_json()["data"]
    qs1 = t1_data["questions"]
    att_id1 = t1_data["attempt_id"]
    assert len(qs1) == 50, f"Expected 50 questions, got {len(qs1)}"
    for q in qs1:
        assert "correct_option" not in q
        assert "correctIndex" not in q
    print(f"  Attempt 1 started: AttemptID='{att_id1}', Question Count={len(qs1)} (answers stripped)")

    print("\n=== TEST 4: User 1 submits Mock Test ===")
    sub_res1 = client.post("/api/tests/sub_dsa/submit", headers={"Authorization": f"Bearer {token1}"}, json={
        "attempt_id": att_id1,
        "submission_reason": "manual",
        "answers": [{"question_id": q["id"], "selected_option": "A"} for q in qs1[:10]],
        "time_taken": 1800
    })
    assert sub_res1.status_code == 200
    result1 = sub_res1.get_json()["data"]
    assert "score" in result1
    print(f"  Attempt 1 submitted: Score={result1['score']}/{result1['total_questions']}, Pct={result1['percentage']}%")

    print("\n=== TEST 5: User 1 starts second Mock Test (DSA) - verifies unseen question rotation ===")
    test_res2 = client.post("/api/tests/sub_dsa/start", headers={"Authorization": f"Bearer {token1}"}, json={
        "length": 50
    })
    assert test_res2.status_code == 200
    qs2 = test_res2.get_json()["data"]["questions"]
    assert len(qs2) == 50
    qs1_ids = set(q["id"] for q in qs1)
    qs2_ids = set(q["id"] for q in qs2)
    # DSA has 100 questions. Attempt 1 had 50. Attempt 2 has the other 50. Overlap must be 0!
    overlap = qs1_ids.intersection(qs2_ids)
    assert len(overlap) == 0, f"Expected 0 overlap between DSA attempts 1 & 2, got {len(overlap)}"
    print(f"  Attempt 2 served {len(qs2)} questions with 0 overlap with Attempt 1! Rotation verified.")

    print("\n=== TEST 6: User 1 logs out ===")
    logout_res = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token1}"})
    assert logout_res.status_code == 200
    print("  User 1 logged out successfully.")

    print("\n=== TEST 7: Register User 2 (Priya Patel) ===")
    user2_payload = {
        "name": "Priya Patel",
        "email": "priya.patel.sim@example.com",
        "password": "Password@123",
        "confirm_password": "Password@123",
        "mobile": "+91 9988776655",
        "location": "Ahmedabad, India",
        "education": "M.Tech CSE"
    }
    r2 = client.post("/api/auth/register", json=user2_payload)
    assert r2.status_code in [201, 409]

    l2 = client.post("/api/auth/login", json={"email": user2_payload["email"], "password": user2_payload["password"]})
    assert l2.status_code == 200
    token2 = l2.get_json()["data"]["token"]
    u2 = l2.get_json()["data"]["user"]
    assert u2["name"] == "Priya Patel"
    assert u2["email"] == user2_payload["email"]
    assert u2["id"] != u1["id"]
    print(f"  User 2 registered and logged in: ID={u2['id']}, Name='{u2['name']}'")

    print("\n=== TEST 8: Verify User 2 Profile does NOT leak User 1 data ===")
    prof2 = client.get("/api/student/profile", headers={"Authorization": f"Bearer {token2}"})
    assert prof2.status_code == 200
    p2_data = prof2.get_json()["data"]["profile"]
    assert p2_data["name"] == "Priya Patel"
    assert p2_data["email"] == user2_payload["email"]
    assert p2_data["location"] == "Ahmedabad, India"
    print(f"  Profile verified for User 2: Name='{p2_data['name']}', Location='{p2_data['location']}'")

    print("\nALL SIMULATION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    run_simulation()

