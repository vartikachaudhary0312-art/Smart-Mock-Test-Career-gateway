import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "users.json"

class UserRepository:
    @staticmethod
    def _load_users() -> list[dict]:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_users(users: list[dict]):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)

    def find_all(self) -> list[dict]:
        return self._load_users()

    def find_by_id(self, user_id: int) -> dict | None:
        users = self._load_users()
        return next((u for u in users if u["id"] == user_id), None)

    def find_by_email(self, email: str) -> dict | None:
        users = self._load_users()
        clean = email.strip().lower()
        return next((u for u in users if u["email"].lower() == clean), None)

    def find_students(self) -> list[dict]:
        users = self._load_users()
        return [u for u in users if u.get("role") == "student"]

    def create(self, user_data: dict) -> dict:
        users = self._load_users()
        new_id = max([u["id"] for u in users], default=0) + 1
        user_data["id"] = new_id
        users.append(user_data)
        self._save_users(users)
        return user_data

    def update(self, user_id: int, update_fields: dict) -> dict | None:
        users = self._load_users()
        for u in users:
            if u["id"] == user_id:
                u.update(update_fields)
                self._save_users(users)
                return u
        return None

    def update_status(self, user_id: int, status: str) -> dict | None:
        return self.update(user_id, {"status": status})
