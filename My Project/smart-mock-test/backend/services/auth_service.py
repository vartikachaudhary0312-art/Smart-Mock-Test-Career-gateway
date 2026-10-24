from datetime import datetime
from backend.repositories.user_repository import UserRepository
from backend.utils.security import hash_password, verify_password, generate_token
from backend.utils.validators import validate_registration_payload, validate_email

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, data: dict, secret_key: str) -> tuple[bool, str, dict | None, int]:
        is_valid, msg = validate_registration_payload(data)
        if not is_valid:
            return False, msg, None, 400

        email = data["email"].strip().lower()
        if self.user_repo.find_by_email(email):
            return False, "An account with this email address already exists.", None, 409

        role = data.get("role", "student")
        if role not in ["student", "admin"]:
            role = "student"

        user_obj = {
            "name": data["name"].strip(),
            "email": email,
            "password_hash": hash_password(data["password"]),
            "role": role,
            "mobile": data.get("mobile", data.get("phone", "")),
            "location": data.get("location", "India"),
            "education": data.get("education", "MCA Student"),
            "skills": data.get("skills", ["Java", "Python", "SQL"]),
            "status": "Active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        created = self.user_repo.create(user_obj)
        token = generate_token({"id": created["id"], "email": created["email"], "role": created["role"]}, secret_key)

        safe_user = {
            "id": created["id"],
            "name": created["name"],
            "email": created["email"],
            "role": created["role"],
            "mobile": created["mobile"],
            "location": created["location"]
        }

        return True, "Registration successful", {"user": safe_user, "token": token}, 201

    def login_user(self, email: str, password: str, secret_key: str, requested_role: str = "student") -> tuple[bool, str, dict | None, int]:
        if not validate_email(email) or not password:
            return False, "Email and password are required.", None, 400

        user = self.user_repo.find_by_email(email)
        if not user or not verify_password(user["password_hash"], password):
            return False, "Invalid email or password.", None, 401

        if user.get("status") == "Blocked":
            return False, "Account is currently suspended. Please contact administrator.", None, 403

        # Strict Backend Role Authorization Check
        actual_role = (user.get("role") or "student").strip().lower()
        req_role = (requested_role or "student").strip().lower()

        if req_role and actual_role != req_role:
            if actual_role == "admin" and req_role == "student":
                return False, "Admin account detected. Please select Admin Login.", None, 403
            elif actual_role == "student" and req_role == "admin":
                return False, "Student account detected. Please select Student Login.", None, 403
            else:
                return False, f"Role mismatch. Credentials belong to a {actual_role} account.", None, 403

        token = generate_token({"id": user["id"], "email": user["email"], "role": actual_role}, secret_key)

        safe_user = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": actual_role,
            "mobile": user.get("mobile", ""),
            "location": user.get("location", "")
        }

        return True, "Login successful", {"user": safe_user, "token": token}, 200

    def get_current_user_profile(self, user_id: int) -> dict | None:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return None
        safe = dict(user)
        safe.pop("password_hash", None)
        return safe
