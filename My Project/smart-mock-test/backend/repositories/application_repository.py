import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "applications.json"

class ApplicationRepository:
    @staticmethod
    def _load_apps() -> list[dict]:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_apps(apps: list[dict]):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(apps, f, indent=2)

    def find_all(self) -> list[dict]:
        return self._load_apps()

    def find_by_id(self, app_id: int) -> dict | None:
        apps = self._load_apps()
        return next((a for a in apps if a["id"] == app_id), None)

    def find_by_student_id(self, student_id: int) -> list[dict]:
        apps = self._load_apps()
        return [a for a in apps if a.get("student_id") == student_id]

    def find_by_student_and_job(self, student_id: int, job_id: int) -> dict | None:
        apps = self._load_apps()
        return next((a for a in apps if a.get("student_id") == student_id and a.get("job_id") == job_id), None)

    def create(self, app_data: dict) -> dict:
        apps = self._load_apps()
        new_id = max([a["id"] for a in apps], default=0) + 1
        app_data["id"] = new_id
        apps.insert(0, app_data)
        self._save_apps(apps)
        return app_data

    def update_status(self, app_id: int, status: str) -> dict | None:
        apps = self._load_apps()
        for a in apps:
            if a["id"] == app_id:
                a["status"] = status
                self._save_apps(apps)
                return a
        return None
