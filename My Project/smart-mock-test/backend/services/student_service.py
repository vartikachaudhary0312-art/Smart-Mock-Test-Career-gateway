from backend.repositories.user_repository import UserRepository

class StudentService:
    def __init__(self):
        self.user_repo = UserRepository()

    def get_profile(self, user_id: int) -> dict | None:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return None
        safe = dict(user)
        safe.pop("password_hash", None)
        return safe

    def update_profile(self, user_id: int, update_data: dict) -> tuple[bool, str, dict | None]:
        allowed_fields = ["name", "mobile", "location", "education", "skills"]
        filtered = {k: v for k, v in update_data.items() if k in allowed_fields}

        updated = self.user_repo.update(user_id, filtered)
        if not updated:
            return False, "Student profile not found.", None

        safe = dict(updated)
        safe.pop("password_hash", None)
        return True, "Profile updated successfully", safe
