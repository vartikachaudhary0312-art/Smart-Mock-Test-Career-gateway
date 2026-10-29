import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "questions.json"

SUBJECT_ALIASES = {
    "java": ["java", "java programming"],
    "python": ["python", "python programming"],
    "dsa": ["dsa", "data structures", "data structures & algorithms", "data structures and algorithms"],
    "dbms": ["dbms", "database management systems", "database management systems (dbms)"],
    "os": ["os", "operating systems"],
    "cn": ["cn", "computer networks"],
    "se": ["se", "software engineering"],
    "toc": ["toc", "theory of computation"],
    "coa": ["coa", "computer organization & architecture", "computer organization and architecture"],
    "ai": ["ai", "artificial intelligence"],
    "ml": ["ml", "machine learning", "machine learning fundamentals"],
    "javascript": ["javascript", "js"],
    "js": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "ts": ["typescript", "ts"],
    "react": ["react", "react.js", "reactjs"],
    "node": ["node", "node.js", "nodejs"],
    "express": ["express", "express.js", "expressjs"],
    "sql": ["sql", "sql & database queries", "sql queries"],
    "quants": ["quantitative aptitude", "quants"],
    "aptitude": ["quantitative aptitude", "logical reasoning", "aptitude"],
    "tcs": ["tcs", "tata consultancy services"]
}

def is_subject_match(q_sub, target_sub, q_sub_id=None, target_sub_id=None) -> bool:
    if not target_sub and not target_sub_id:
        return True
    
    t_sub_id_str = str(target_sub_id or "").strip().lower()
    q_sub_id_str = str(q_sub_id or "").strip().lower()
    t_s = str(target_sub or "").strip().lower()
    q_s = str(q_sub or "").strip().lower()

    if t_sub_id_str and q_sub_id_str and t_sub_id_str == q_sub_id_str:
        return True
    if t_s and (t_s == q_s or t_s == q_sub_id_str):
        return True
    if t_sub_id_str and (t_sub_id_str == q_s or t_sub_id_str == q_sub_id_str):
        return True

    for key, alias_list in SUBJECT_ALIASES.items():
        if (t_s == key or t_s in alias_list) and (q_s == key or q_s in alias_list):
            return True
            
    return False

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

    def find_by_id(self, question_id) -> dict | None:
        questions = self._load_questions()
        return next((q for q in questions if str(q["id"]) == str(question_id)), None)

    def filter(self, subject: str = None, subject_id = None, difficulty: str = None) -> list[dict]:
        questions = self._load_questions()
        filtered = []
        for q in questions:
            match_sub = True
            if subject_id is not None or subject is not None:
                match_sub = is_subject_match(q.get("subject", ""), subject, q.get("subject_id"), subject_id)
            
            match_diff = True
            if difficulty and difficulty.lower() != "mixed":
                match_diff = str(q.get("difficulty", "")).lower() == difficulty.strip().lower()

            if match_sub and match_diff:
                filtered.append(q)

        return filtered

    def create(self, q_data: dict) -> dict:
        questions = self._load_questions()
        new_id = max([q["id"] for q in questions if isinstance(q.get("id"), int)], default=0) + 1
        q_data.setdefault("id", new_id)
        questions.append(q_data)
        self._save_questions(questions)
        return q_data

    def update(self, question_id, update_fields: dict) -> dict | None:
        questions = self._load_questions()
        for q in questions:
            if str(q["id"]) == str(question_id):
                q.update(update_fields)
                self._save_questions(questions)
                return q
        return None

    def delete(self, question_id) -> bool:
        questions = self._load_questions()
        initial_len = len(questions)
        questions = [q for q in questions if str(q["id"]) != str(question_id)]
        if len(questions) < initial_len:
            self._save_questions(questions)
            return True
        return False
