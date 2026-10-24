import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "questions.json"

class QuestionRepository:
    @staticmethod
    def _load_questions() -> list[dict]:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_questions(questions: list[dict]):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2)

    def find_all(self) -> list[dict]:
        return self._load_questions()

    def find_by_id(self, question_id: int) -> dict | None:
        questions = self._load_questions()
        return next((q for q in questions if q["id"] == question_id), None)

    def filter(self, subject: str = None, subject_id: int = None, difficulty: str = None) -> list[dict]:
        questions = self._load_questions()
        filtered = []
        for q in questions:
            match_sub = True
            if subject_id is not None:
                match_sub = q.get("subject_id") == subject_id
            elif subject:
                match_sub = str(q.get("subject", "")).lower() == subject.strip().lower() or str(q.get("subject_id", "")).lower() == subject.strip().lower()
            
            match_diff = True
            if difficulty:
                match_diff = q.get("difficulty", "").lower() == difficulty.strip().lower()

            if match_sub and match_diff:
                filtered.append(q)

        return filtered

    def create(self, q_data: dict) -> dict:
        questions = self._load_questions()
        new_id = max([q["id"] for q in questions], default=0) + 1
        q_data["id"] = new_id
        questions.append(q_data)
        self._save_questions(questions)
        return q_data

    def update(self, question_id: int, update_fields: dict) -> dict | None:
        questions = self._load_questions()
        for q in questions:
            if q["id"] == question_id:
                q.update(update_fields)
                self._save_questions(questions)
                return q
        return None

    def delete(self, question_id: int) -> bool:
        questions = self._load_questions()
        initial_len = len(questions)
        questions = [q for q in questions if q["id"] != question_id]
        if len(questions) < initial_len:
            self._save_questions(questions)
            return True
        return False
