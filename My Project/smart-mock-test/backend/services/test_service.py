import time
import random
from datetime import datetime
from backend.repositories.test_repository import TestRepository
from backend.repositories.question_repository import QuestionRepository, is_subject_match
from backend.repositories.result_repository import ResultRepository
from backend.repositories.attempt_repository import AttemptRepository
from backend.repositories.security_event_repository import SecurityEventRepository

class TestService:
    __test__ = False

    SECURITY_POLICY = {
        "face_missing": {"max_violations": 3, "grace_seconds": 5},
        "multiple_faces": {"max_violations": 2, "grace_seconds": 3},
        "tab_switch": {"max_violations": 3, "grace_seconds": 1},
        "fullscreen_exit": {"max_violations": 2, "grace_seconds": 0},
        "clipboard_attempt": {"max_violations": 3, "grace_seconds": 0},
        "camera_disconnect": {"max_violations": 2, "grace_seconds": 5},
        "max_total_violations": 6,
        "enforce_fullscreen": True,
        "block_clipboard": True,
        "block_context_menu": True,
        "monitor_camera": True,
        "monitor_tab_switch": True
    }

    def __init__(self):
        self.test_repo = TestRepository()
        self.question_repo = QuestionRepository()
        self.result_repo = ResultRepository()
        self.attempt_repo = AttemptRepository()
        self.security_event_repo = SecurityEventRepository()

    def get_all_categories(self) -> list[dict]:
        return self.test_repo.find_all_categories()

    def get_category_by_id(self, cat_id: str) -> dict | None:
        cat = self.test_repo.find_category_by_id(cat_id)
        if not cat:
            return None
        subjects = self.test_repo.find_all_subjects()
        cat_topics = [s for s in subjects if s.get("category_id") == cat["id"] or s.get("category") == cat["name"]]
        cat_copy = dict(cat)
        cat_copy["topics"] = cat_topics
        return cat_copy

    def get_all_subjects(self, category_id: str = None) -> list[dict]:
        subjects = self.test_repo.find_all_subjects()
        if category_id:
            c_lower = category_id.strip().lower()
            return [s for s in subjects if str(s.get("category_id", "")).lower() == c_lower or str(s.get("category", "")).lower() == c_lower]
        return subjects

    def get_tests(self, subject: str = None, difficulty: str = None) -> list[dict]:
        return self.test_repo.filter(subject=subject, difficulty=difficulty)

    def get_test_by_id(self, test_id) -> dict | None:
        test = self.test_repo.find_by_id(test_id)
        if test:
            return test
        # Fallback for dynamic topic/subject IDs or codes
        subjects = self.test_repo.find_all_subjects()
        matched_sub = next(
            (s for s in subjects if str(s.get("id", "")).lower() == str(test_id).lower() or 
                                     str(s.get("code", "")).lower() == str(test_id).lower() or
                                     str(s.get("name", "")).lower() == str(test_id).lower()),
            None
        )
        if matched_sub:
            return {
                "id": matched_sub["id"],
                "title": f"{matched_sub['name']} Mock Test",
                "subject": matched_sub["name"],
                "subject_id": matched_sub["id"],
                "category_id": matched_sub.get("category_id", "cat_core_cs"),
                "category": matched_sub.get("category", "Core Computer Science"),
                "difficulty": matched_sub.get("difficulty", "medium"),
                "duration_minutes": matched_sub.get("defaultDuration", matched_sub.get("duration_minutes", 30)),
                "question_count": matched_sub.get("question_count", 0),
                "topics": matched_sub.get("topics", []),
                "description": matched_sub.get("description", "")
            }
        return None

    def get_practice_questions(self, test_id, difficulty: str = None, length: int = None) -> tuple[bool, str, list | None, int]:
        test = self.get_test_by_id(test_id)
        if not test:
            return False, f"Topic or subject '{test_id}' not found.", None, 404

        target_subject = test.get("subject")
        target_subject_id = test.get("subject_id") or test.get("id")
        effective_diff = difficulty
        if effective_diff and str(effective_diff).lower() == "mixed":
            effective_diff = None

        questions = self.question_repo.filter(subject=target_subject, subject_id=target_subject_id, difficulty=effective_diff)
        if not questions and effective_diff is not None:
            questions = self.question_repo.filter(subject=target_subject, subject_id=target_subject_id, difficulty=None)

        if not questions:
            return False, f"Questions coming soon for this topic ({target_subject}).", None, 404

        if length and isinstance(length, int) and length > 0:
            questions = questions[:length]

        # For practice mode, include explanation and correct_option so student gets immediate feedback!
        practice_questions = []
        for q in questions:
            pq = {
                "id": q["id"],
                "subject": q.get("subject", target_subject),
                "subject_id": q.get("subject_id", target_subject_id),
                "question_text": q.get("question_text", q.get("question", "")),
                "option_a": q.get("option_a", q.get("options", [""])[0] if len(q.get("options", [])) > 0 else ""),
                "option_b": q.get("option_b", q.get("options", ["", ""])[1] if len(q.get("options", [])) > 1 else ""),
                "option_c": q.get("option_c", q.get("options", ["", "", ""])[2] if len(q.get("options", [])) > 2 else ""),
                "option_d": q.get("option_d", q.get("options", ["", "", "", ""])[3] if len(q.get("options", [])) > 3 else ""),
                "options": q.get("options", [
                    q.get("option_a", ""), q.get("option_b", ""), q.get("option_c", ""), q.get("option_d", "")
                ]),
                "correct_option": q.get("correct_option", "A"),
                "correctIndex": q.get("correctIndex", 0),
                "explanation": q.get("explanation", "Correct answer is " + q.get("correct_option", "A")),
                "difficulty": q.get("difficulty", "medium")
            }
            practice_questions.append(pq)

        return True, "Practice questions retrieved successfully.", practice_questions, 200

    def start_test(self, test_id, user_id: int = None, difficulty: str = None, length: int = None) -> tuple[bool, str, dict | None, int]:
        test = self.get_test_by_id(test_id)
        if not test:
            return False, f"Test instance or subject with ID '{test_id}' not found.", None, 404

        target_subject = test.get("subject")
        target_subject_id = test.get("subject_id") or test.get("id")
        effective_diff = difficulty
        if effective_diff and str(effective_diff).lower() in ["mixed", "all", "any"]:
            effective_diff = None

        # 1. Fetch matching questions for this subject
        all_sub_questions = self.question_repo.filter(subject=target_subject, subject_id=target_subject_id, difficulty=None)
        if not all_sub_questions:
            if str(target_subject).lower() in ["all", "comprehensive", "full syllabus"]:
                all_sub_questions = self.question_repo.find_all()
            else:
                return False, f"Questions coming soon for this subject ({target_subject}).", None, 404

        target_len = length if (length and isinstance(length, int) and length > 0) else min(50, len(all_sub_questions))

        if effective_diff:
            diff_questions = self.question_repo.filter(subject=target_subject, subject_id=target_subject_id, difficulty=effective_diff)
            if not diff_questions:
                # If requested difficulty level is not yet populated, use all questions for this subject
                questions = all_sub_questions
            elif len(diff_questions) < target_len:
                # Prioritize requested difficulty and backfill remainder from same subject
                diff_ids = {d["id"] for d in diff_questions}
                other_questions = [q for q in all_sub_questions if q["id"] not in diff_ids]
                questions = diff_questions + other_questions
            else:
                questions = diff_questions
        else:
            questions = all_sub_questions

        # 4. Track previously served question IDs per user and subject to prefer unseen questions
        seen_qids = set()
        recent_qids = set()
        if user_id:
            try:
                user_attempts = self.attempt_repo.find_by_user_id(user_id)
                # Find most recent attempt for this test/subject
                for att in user_attempts:
                    if str(att.get("test_id", "")).lower() == str(test_id).lower() or is_subject_match(str(att.get("test_id", "")), target_subject):
                        recent_qids = set(str(qid) for qid in att.get("question_ids", []))
                        break

                for att in user_attempts:
                    for qid in att.get("question_ids", []):
                        seen_qids.add(str(qid))
            except Exception:
                pass

        # Partition into:
        # 1. Unseen: questions never served to this user before
        # 2. Seen older: questions served in older attempts, but NOT in the most recent attempt
        # 3. Seen recent: questions served in the immediately preceding attempt
        unseen = [q for q in questions if str(q["id"]) not in seen_qids]
        seen_older = [q for q in questions if str(q["id"]) in seen_qids and str(q["id"]) not in recent_qids]
        seen_recent = [q for q in questions if str(q["id"]) in recent_qids]

        random.shuffle(unseen)
        random.shuffle(seen_older)
        random.shuffle(seen_recent)

        # Target question length: default to 50 if length is not specified or None
        target_len = length if (length and isinstance(length, int) and length > 0) else min(50, len(questions))

        selected_pool = unseen + seen_older + seen_recent
        selected_questions = selected_pool[:target_len]
        random.shuffle(selected_questions)

        # Strip correct answers from questions sent to student before submission
        stripped_questions = []
        for q in selected_questions:
            sq = {
                "id": q["id"],
                "subject": q.get("subject", target_subject),
                "subject_id": q.get("subject_id", target_subject_id),
                "question_text": q.get("question_text", q.get("question", "")),
                "option_a": q.get("option_a", q.get("options", [""])[0] if len(q.get("options", [])) > 0 else ""),
                "option_b": q.get("option_b", q.get("options", ["", ""])[1] if len(q.get("options", [])) > 1 else ""),
                "option_c": q.get("option_c", q.get("options", ["", "", ""])[2] if len(q.get("options", [])) > 2 else ""),
                "option_d": q.get("option_d", q.get("options", ["", "", "", ""])[3] if len(q.get("options", [])) > 3 else ""),
                "options": q.get("options", [
                    q.get("option_a", ""), q.get("option_b", ""), q.get("option_c", ""), q.get("option_d", "")
                ]),
                "difficulty": q.get("difficulty", "medium")
            }
            stripped_questions.append(sq)

        attempt_id = f"att_{int(time.time())}_{test_id}_{user_id or 0}"
        attempt_record = {
            "attempt_id": attempt_id,
            "test_id": test_id,
            "user_id": user_id,
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "in_progress",
            "question_ids": [q["id"] for q in stripped_questions],
            "violations_count": 0,
            "violations_breakdown": {},
            "submission_reason": None,
            "result_id": None
        }
        self.attempt_repo.create(attempt_record)

        test_info = dict(test)
        test_info["question_count"] = len(stripped_questions)
        if difficulty:
            test_info["difficulty"] = difficulty

        payload = {
            "attempt_id": attempt_id,
            "test": test_info,
            "questions": stripped_questions,
            "security_policy": self.SECURITY_POLICY
        }

        return True, "Test initialized successfully", payload, 200

    def log_security_event(self, user_id: int, test_id, payload: dict) -> tuple[bool, str, dict | None, int]:
        attempt_id = payload.get("attempt_id")
        if not attempt_id:
            return False, "Missing attempt_id in security event payload.", None, 400

        attempt = self.attempt_repo.find_by_id(attempt_id)
        if not attempt:
            return False, f"Test attempt {attempt_id} not found.", None, 404

        if attempt.get("user_id") and attempt.get("user_id") != user_id:
            return False, "Unauthorized access to this test attempt.", None, 403

        if attempt.get("status") == "submitted":
            return False, "Cannot log security events for an already submitted attempt.", None, 409

        event_type = payload.get("event_type", "generic_warning").strip().lower()
        client_timestamp = payload.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        details = payload.get("details", {})
        if not isinstance(details, dict):
            details = {"message": str(details)}
        sanitized_details = {k: v for k, v in details.items() if k not in ["imageData", "image_data", "camera_frame", "token"]}

        event_record = {
            "attempt_id": attempt_id,
            "user_id": user_id,
            "test_id": test_id,
            "event_type": event_type,
            "severity": payload.get("severity", "warning"),
            "timestamp": client_timestamp,
            "details": sanitized_details
        }
        saved_event = self.security_event_repo.create(event_record)

        violations_breakdown = attempt.get("violations_breakdown", {})
        violations_breakdown[event_type] = violations_breakdown.get(event_type, 0) + 1
        total_violations = sum(violations_breakdown.values())

        should_auto_submit = False
        auto_submit_reason = None

        policy_for_type = self.SECURITY_POLICY.get(event_type, {})
        max_allowed = policy_for_type.get("max_violations")
        if max_allowed and violations_breakdown[event_type] >= max_allowed:
            should_auto_submit = True
            auto_submit_reason = f"Security violation limit exceeded: {event_type} ({violations_breakdown[event_type]}/{max_allowed})"
        elif total_violations >= self.SECURITY_POLICY.get("max_total_violations", 6):
            should_auto_submit = True
            auto_submit_reason = f"Total cumulative security violations exceeded ({total_violations}/{self.SECURITY_POLICY.get('max_total_violations')})"

        self.attempt_repo.update(attempt_id, {
            "violations_count": total_violations,
            "violations_breakdown": violations_breakdown,
            "last_event_at": client_timestamp
        })

        response_data = {
            "event_id": saved_event.get("id"),
            "attempt_id": attempt_id,
            "event_type": event_type,
            "current_violation_count": violations_breakdown[event_type],
            "total_violations": total_violations,
            "should_auto_submit": should_auto_submit,
            "auto_submit_reason": auto_submit_reason
        }

        return True, "Security event recorded successfully.", response_data, 200

    def get_attempt_details(self, attempt_id: str, user_id: int, role: str = "student") -> tuple[bool, str, dict | None, int]:
        attempt = self.attempt_repo.find_by_id(attempt_id)
        if not attempt:
            return False, f"Test attempt {attempt_id} not found.", None, 404

        if role != "admin" and attempt.get("user_id") and attempt.get("user_id") != user_id:
            return False, "Access denied to this attempt data.", None, 403

        events = self.security_event_repo.find_by_attempt_id(attempt_id)
        result_data = None
        if attempt.get("result_id"):
            result_data = self.result_repo.find_by_id(attempt.get("result_id"))

        data = {
            "attempt": attempt,
            "events": events,
            "result": result_data
        }
        return True, "Attempt details retrieved successfully.", data, 200

    def submit_test(self, user_id: int, test_id, payload: dict) -> tuple[bool, str, dict | None, int]:
        attempt_id = payload.get("attempt_id")
        attempt = None

        if attempt_id:
            attempt = self.attempt_repo.find_by_id(attempt_id)
            if attempt:
                if attempt.get("user_id") and attempt.get("user_id") != user_id:
                    return False, "Unauthorized: Attempt does not belong to the current authenticated student.", None, 403

                if attempt.get("status") == "submitted":
                    return False, "This test attempt has already been submitted and finalized.", None, 409

        submission_reason = payload.get("submission_reason", "manual")
        user_answers = payload.get("answers", [])
        time_taken = payload.get("time_taken", payload.get("timeSpentMinutes", 15))

        test = self.get_test_by_id(test_id)
        subject_name = test.get("subject") if test else payload.get("subjectName", "Computer Science")
        difficulty = test.get("difficulty") if test else payload.get("difficulty", "medium")

        all_questions = self.question_repo.find_all()
        q_map = {str(q["id"]): q for q in all_questions}

        answers_dict = {}
        if isinstance(user_answers, list):
            for ans in user_answers:
                if isinstance(ans, dict):
                    answers_dict[str(ans.get("question_id"))] = str(ans.get("selected_option", "")).upper()
        elif isinstance(user_answers, dict):
            for q_id_str, opt in user_answers.items():
                answers_dict[str(q_id_str)] = str(opt).upper()

        attempt_q_ids = attempt.get("question_ids") if attempt else None
        if attempt_q_ids:
            relevant_questions = [q_map[str(qid)] for qid in attempt_q_ids if str(qid) in q_map]
        else:
            relevant_questions = [q for q in all_questions if is_subject_match(q.get("subject", ""), subject_name, q.get("subject_id"), test.get("id") if test else None)]
            if not relevant_questions:
                ans_ids = list(answers_dict.keys())
                if ans_ids:
                    relevant_questions = [q_map[str(qid)] for qid in ans_ids if str(qid) in q_map]
                if not relevant_questions:
                    relevant_questions = all_questions[:10]

        correct_answers = 0
        wrong_answers = 0
        skipped_answers = 0
        total_questions = len(relevant_questions)

        for q in relevant_questions:
            q_id = str(q["id"])
            selected = answers_dict.get(q_id)
            correct_opt = str(q.get("correct_option", q.get("correctIndex", "A"))).upper()

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

        violations_count = 0
        security_summary = payload.get("security_summary", {})
        if attempt:
            violations_count = attempt.get("violations_count", 0)
        elif "violations_count" in payload:
            violations_count = int(payload.get("violations_count", 0))

        result_record = {
            "user_id": user_id,
            "test_id": test_id,
            "attempt_id": attempt_id,
            "submission_reason": submission_reason,
            "violations_count": violations_count,
            "security_summary": security_summary,
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

        if attempt_id:
            self.attempt_repo.update(attempt_id, {
                "status": "submitted",
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "submission_reason": submission_reason,
                "result_id": created_result["id"]
            })

        return True, "Test submitted and evaluated successfully", created_result, 200
