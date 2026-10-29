import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "test_attempts.json"

class AttemptRepository:
    """Repository for managing test attempts and sessions in JSON storage."""

    @staticmethod
    def _load_attempts() -> list[dict]:
        if not DATA_FILE.exists():
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def _save_attempts(attempts: list[dict]):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(attempts, f, indent=2)

    def find_all(self) -> list[dict]:
        return self._load_attempts()

    def find_by_id(self, attempt_id: str) -> dict | None:
        attempts = self._load_attempts()
        return next((a for a in attempts if str(a.get("attempt_id")) == str(attempt_id)), None)

    def find_by_user_id(self, user_id: int) -> list[dict]:
        attempts = self._load_attempts()
        return [a for a in attempts if a.get("user_id") == user_id]

    def create(self, attempt_data: dict) -> dict:
        attempts = self._load_attempts()
        # Default fields
        if "created_at" not in attempt_data:
            attempt_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "status" not in attempt_data:
            attempt_data["status"] = "in_progress"
        if "violations_count" not in attempt_data:
            attempt_data["violations_count"] = 0

        attempts.insert(0, attempt_data)
        self._save_attempts(attempts)
        return attempt_data

    def update(self, attempt_id: str, updates: dict) -> dict | None:
        attempts = self._load_attempts()
        for idx, a in enumerate(attempts):
            if str(a.get("attempt_id")) == str(attempt_id):
                attempts[idx].update(updates)
                self._save_attempts(attempts)
                return attempts[idx]
        return None

