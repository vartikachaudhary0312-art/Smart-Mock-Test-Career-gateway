import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "security_events.json"

class SecurityEventRepository:
    """Repository for storing and querying anti-cheating proctoring events."""

    @staticmethod
    def _load_events() -> list[dict]:
        if not DATA_FILE.exists():
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def _save_events(events: list[dict]):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)

    def find_all(self) -> list[dict]:
        return self._load_events()

    def find_by_attempt_id(self, attempt_id: str) -> list[dict]:
        events = self._load_events()
        return [e for e in events if str(e.get("attempt_id")) == str(attempt_id)]

    def find_by_user_id(self, user_id: int) -> list[dict]:
        events = self._load_events()
        return [e for e in events if e.get("user_id") == user_id]

    def create(self, event_data: dict) -> dict:
        events = self._load_events()
        new_id = max([e.get("id", 0) for e in events], default=0) + 1
        event_data["id"] = new_id
        if "timestamp" not in event_data or not event_data["timestamp"]:
            event_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        events.append(event_data)
        self._save_events(events)
        return event_data

