import os
from datetime import datetime
from flask import current_app
from backend.repositories.user_repository import UserRepository
from backend.utils.security import hash_password, verify_password, generate_token
from backend.utils.validators import validate_registration_payload, validate_email

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def provision_admin_account(self, admin_email: str, admin_password: str) -> dict:
        """
        Ensures the configured single Admin account exists and its password hash
        matches the configured ADMIN_PASSWORD using secure hashing.
        Also demotes any other accounts that may previously have claimed the 'admin' role.
        """
        admin_email = admin_email.strip().lower()

        # Demote any other unauthorized accounts claiming 'admin'
        all_users = self.user_repo.find_all()
        for u in all_users:
            if u.get("role") == "admin" and (u.get("email") or "").strip().lower() != admin_email:
                u["role"] = "student"
                self.user_repo.update(u["id"], u)

        admin_user = self.user_repo.find_by_email(admin_email)
        if not admin_user:
            admin_user = {
                "name": "System Administrator",
                "email": admin_email,
                "password_hash": hash_password(admin_password) if admin_password else "",
                "role": "admin",
                "mobile": "+91 9876543211",
                "location": "New Delhi, India",
                "education": "System Administration Specialist",
                "skills": ["Administration", "Security", "Flask"],
                "status": "Active",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            admin_user = self.user_repo.create(admin_user)
        else:
            needs_update = False
            if admin_user.get("role") != "admin":
                admin_user["role"] = "admin"
                needs_update = True
            if admin_password:
                current_hash = admin_user.get("password_hash", "")
                if not current_hash or not verify_password(current_hash, admin_password):
                    admin_user["password_hash"] = hash_password(admin_password)
                    needs_update = True
            if needs_update:
                self.user_repo.update(admin_user["id"], admin_user)

        return admin_user

    def register_user(self, data: dict, secret_key: str) -> tuple[bool, str, dict | None, int]:
        is_valid, msg = validate_registration_payload(data)
        if not is_valid:
            return False, msg, None, 400

        email = data["email"].strip().lower()
        admin_email = current_app.config.get("ADMIN_EMAIL", "vartikachaudhary0312@gmail.com").strip().lower()

        # Prevent registering the reserved Admin email through public registration
        if email == admin_email:
            return False, "This email address is reserved for system administration.", None, 403

        if self.user_repo.find_by_email(email):
            return False, "An account with this email address already exists.", None, 409

        # Public registration is strictly for students; users cannot self-assign admin roles
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

        email = email.strip().lower()
        req_role = (requested_role or "student").strip().lower()
        admin_email = current_app.config.get("ADMIN_EMAIL", "vartikachaudhary0312@gmail.com").strip().lower()
        admin_password_env = (current_app.config.get("ADMIN_PASSWORD") or os.getenv("ADMIN_PASSWORD") or "").strip()

        # Admin login branch
        if req_role == "admin":
            if email != admin_email:
                return False, "Access denied. Only the designated administrator account is authorized.", None, 403

            if not admin_password_env:
                return False, "Admin password is not configured on the server. Please set ADMIN_PASSWORD in environment.", None, 503

            # Provision / sync admin credentials with configured ADMIN_PASSWORD
            admin_user = self.provision_admin_account(admin_email, admin_password_env)

            if not verify_password(admin_user["password_hash"], password):
                return False, "Invalid email or password.", None, 401

            if admin_user.get("status") == "Blocked":
                return False, "Account is currently suspended. Please contact administrator.", None, 403

            token = generate_token({"id": admin_user["id"], "email": admin_email, "role": "admin"}, secret_key)
            safe_user = {
                "id": admin_user["id"],
                "name": admin_user.get("name", "System Administrator"),
                "email": admin_email,
                "role": "admin",
                "mobile": admin_user.get("mobile", ""),
                "location": admin_user.get("location", "")
            }
            return True, "Login successful", {"user": safe_user, "token": token}, 200

        # Student login branch
        if email == admin_email:
            return False, "Admin account detected. Please select Admin Login.", None, 403

        user = self.user_repo.find_by_email(email)
        if not user or not verify_password(user["password_hash"], password):
            return False, "Invalid email or password.", None, 401

        if user.get("status") == "Blocked":
            return False, "Account is currently suspended. Please contact administrator.", None, 403

        actual_role = (user.get("role") or "student").strip().lower()
        if actual_role != "student":
            return False, "Role mismatch. Please select the correct login role.", None, 403

        token = generate_token({"id": user["id"], "email": user["email"], "role": "student"}, secret_key)

        safe_user = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": "student",
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
