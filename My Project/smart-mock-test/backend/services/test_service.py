import time
from datetime import datetime
from backend.repositories.test_repository import TestRepository
from backend.repositories.question_repository import QuestionRepository
from backend.repositories.result_repository import ResultRepository

class TestService:
    __test__ = False

    def __init__(self):
        self.test_repo = TestRepository()
        self.question_repo = QuestionRepository()
        self.result_repo = ResultRepository()

    def get_all_subjects(self):
        return self.test_repo.find_all_subjects()

    def get_tests(self, subject: str = None, difficulty: str = None) -> list[dict]:
        return self.test_repo.filter(subject=subject, difficulty=difficulty)

    def get_test_by_id(self, test_id: int) -> dict | None:
        return self.test_repo.find_by_id(test_id)

    def start_test(self, test_id: int) -> tuple[bool, str, dict | None, int]:
        test = self.test_repo.find_by_id(test_id)
        if not test:
            # Fallback for dynamic subject IDs if matching subject code
            subjects = self.test_repo.find_all_subjects()
            matched_sub = next((s for s in subjects if s["id"] == test_id or str(s.get("code", "")).lower() == str(test_id).lower()), None)
            if matched_sub:
                test = {
                    "id": matched_sub["id"],
                    "title": f"{matched_sub['name']} Test",
                    "subject": matched_sub["name"],
                    "difficulty": "medium",
                    "duration_minutes": 60,
                    "question_count": 10
                }

        if not test:
            return False, f"Test instance with ID {test_id} not found.", None, 404

        questions = self.question_repo.filter(subject=test.get("subject"), difficulty=test.get("difficulty"))
        if not questions:
            questions = self.question_repo.find_all()

        # IMPORTANT: Strip correct answer key from questions sent to student BEFORE submission!
        stripped_questions = []
        for q in questions:
            sq = {
                "id": q["id"],
                "question_text": q.get("question_text", q.get("question", "")),
                "option_a": q.get("option_a", q.get("options", [""])[0] if len(q.get("options", [])) > 0 else ""),
                "option_b": q.get("option_b", q.get("options", ["", ""])[1] if len(q.get("options", [])) > 1 else ""),
                "option_c": q.get("option_c", q.get("options", ["", "", ""])[2] if len(q.get("options", [])) > 2 else ""),
                "option_d": q.get("option_d", q.get("options", ["", "", "", ""])[3] if len(q.get("options", [])) > 3 else ""),
                "difficulty": q.get("difficulty", "medium")
            }
            stripped_questions.append(sq)

        attempt_id = f"att_{int(time.time())}_{test_id}"
        payload = {
            "attempt_id": attempt_id,
            "test": test,
            "questions": stripped_questions
        }

        return True, "Test initialized successfully", payload, 200

    def submit_test(self, user_id: int, test_id: int, payload: dict) -> tuple[bool, str, dict | None, int]:
        user_answers = payload.get("answers", []) # list of {"question_id": 1, "selected_option": "A"} or dict
        time_taken = payload.get("time_taken", payload.get("timeSpentMinutes", 15))

        test = self.test_repo.find_by_id(test_id)
        subject_name = test.get("subject") if test else "Computer Science"
        difficulty = test.get("difficulty") if test else "medium"

        # Load authoritative questions with correct answers from repository
        all_questions = self.question_repo.find_all()
        q_map = {q["id"]: q for q in all_questions}

        # Normalize answers structure
        answers_dict = {}
        if isinstance(user_answers, list):
            for ans in user_answers:
                answers_dict[ans.get("question_id")] = str(ans.get("selected_option", "")).upper()
        elif isinstance(user_answers, dict):
            for q_id_str, opt in user_answers.items():
                try:
                    answers_dict[int(q_id_str)] = str(opt).upper()
                except ValueError:
                    pass

        correct_answers = 0
        wrong_answers = 0
        skipped_answers = 0

        # Calculate result server-side
        relevant_questions = [q for q in all_questions if q.get("subject", "").lower() == subject_name.lower()]
        if not relevant_questions:
            relevant_questions = all_questions[:10]

        total_questions = len(relevant_questions)

        for q in relevant_questions:
            q_id = q["id"]
            selected = answers_dict.get(q_id)
            correct_opt = str(q.get("correct_option", q.get("correctIndex", "A"))).upper()
            
            # Translate 0, 1, 2, 3 to A, B, C, D if needed
            option_map = {"0": "A", "1": "B", "2": "C", "3": "D"}
            if correct_opt in option_map:
                correct_opt = option_map[correct_opt]
            if selected in option_map:
                selected = option_map[selected]

            if not selected or selected == "NONE":
                skipped_answers += 1
            elif selected == correct_opt:
                correct_answers += 1
            else:
                wrong_answers += 1

        score = correct_answers
        percentage = round((correct_answers / total_questions * 100), 1) if total_questions > 0 else 0.0
        attempted = correct_answers + wrong_answers
        accuracy = round((correct_answers / attempted * 100), 1) if attempted > 0 else 0.0

        result_record = {
            "user_id": user_id,
            "test_id": test_id,
            "subject": subject_name,
            "difficulty": difficulty,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "wrong_answers": wrong_answers,
            "skipped_answers": skipped_answers,
            "score": score,
            "percentage": percentage,
            "accuracy": accuracy,
            "time_taken": time_taken,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        created_result = self.result_repo.create(result_record)
        return True, "Test submitted and evaluated successfully", created_result, 200
