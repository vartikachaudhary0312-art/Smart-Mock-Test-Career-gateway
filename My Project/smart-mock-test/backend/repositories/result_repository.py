import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "results.json"

class ResultRepository:
    @staticmethod
    def _load_results() -> list[dict]:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_results(results: list[dict]):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    def find_all(self) -> list[dict]:
        return self._load_results()

    def find_by_id(self, result_id: int) -> dict | None:
        results = self._load_results()
        return next((r for r in results if r["id"] == result_id), None)

    def find_by_user_id(self, user_id: int) -> list[dict]:
        results = self._load_results()
        return [r for r in results if r.get("user_id") == user_id]

    def create(self, result_data: dict) -> dict:
        results = self._load_results()
        new_id = max([r["id"] for r in results], default=0) + 1
        result_data["id"] = new_id
        results.insert(0, result_data)
        self._save_results(results)
        return result_data
