import json
from pathlib import Path

TESTS_FILE = Path(__file__).resolve().parent.parent / "data" / "tests.json"
SUBJECTS_FILE = Path(__file__).resolve().parent.parent / "data" / "subjects.json"
CATEGORIES_FILE = Path(__file__).resolve().parent.parent / "data" / "categories.json"

class TestRepository:
    __test__ = False

    @staticmethod
    def _load_tests() -> list[dict]:
        if not TESTS_FILE.exists():
            return []
        with open(TESTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _load_subjects() -> list[dict]:
        if not SUBJECTS_FILE.exists():
            return []
        with open(SUBJECTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _load_categories() -> list[dict]:
        if not CATEGORIES_FILE.exists():
            return []
        with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_subjects(subjects: list[dict]):
        SUBJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SUBJECTS_FILE, "w", encoding="utf-8") as f:
            json.dump(subjects, f, indent=2)

    def find_all(self) -> list[dict]:
        return self._load_tests()

    def find_all_subjects(self) -> list[dict]:
        return self._load_subjects()

    def find_all_categories(self) -> list[dict]:
        return self._load_categories()

    def find_category_by_id(self, cat_id) -> dict | None:
        categories = self._load_categories()
        c_id_lower = str(cat_id).strip().lower()
        return next((c for c in categories if str(c.get("id", "")).lower() == c_id_lower or str(c.get("slug", "")).lower() == c_id_lower or str(c.get("name", "")).lower() == c_id_lower), None)

    def find_by_id(self, test_id) -> dict | None:
        tests = self._load_tests()
        return next((t for t in tests if str(t["id"]).lower() == str(test_id).lower()), None)

    def filter(self, subject: str = None, difficulty: str = None) -> list[dict]:
        tests = self._load_tests()
        res = []
        for t in tests:
            match_sub = True
            if subject:
                match_sub = t.get("subject", "").lower() == subject.strip().lower()
            match_diff = True
            if difficulty and difficulty.lower() != "mixed":
                match_diff = t.get("difficulty", "").lower() == difficulty.strip().lower()
            if match_sub and match_diff:
                res.append(t)
        return res

    def create_subject(self, sub_data: dict) -> dict:
        subjects = self._load_subjects()
        numeric_ids = [s["id"] for s in subjects if isinstance(s.get("id"), int)]
        new_id = max(numeric_ids, default=0) + 1
        sub_data.setdefault("id", new_id)
        subjects.append(sub_data)
        self._save_subjects(subjects)
        return sub_data
