from flask import Blueprint, request
from backend.services.admin_service import AdminService
from backend.services.student_service import StudentService
from backend.services.job_service import JobService
from backend.services.application_service import ApplicationService
from backend.repositories.question_repository import QuestionRepository
from backend.repositories.result_repository import ResultRepository
from backend.repositories.test_repository import TestRepository
from backend.utils.responses import success_response, error_response
from backend.utils.decorators import role_required
from backend.utils.validators import validate_question_payload

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")

admin_service = AdminService()
student_service = StudentService()
job_service = JobService()
app_service = ApplicationService()
question_repo = QuestionRepository()
result_repo = ResultRepository()
test_repo = TestRepository()

@admin_bp.route("/dashboard", methods=["GET"])
@role_required("admin")
def get_dashboard():
    metrics = admin_service.get_dashboard_metrics()
    return success_response(data=metrics)

@admin_bp.route("/students", methods=["GET"])
@role_required("admin")
def get_students():
    students = admin_service.user_repo.find_students()
    safe_students = []
    for s in students:
        cp = dict(s)
        cp.pop("password_hash", None)
        safe_students.append(cp)
    return success_response(data=safe_students)

@admin_bp.route("/students/<int:student_id>", methods=["GET"])
@role_required("admin")
def get_student_detail(student_id):
    student = student_service.get_profile(student_id)
    if not student or student.get("role") != "student":
        return error_response(message=f"Student #{student_id} not found", status_code=404)
    return success_response(data=student)

@admin_bp.route("/students/<int:student_id>/status", methods=["PUT"])
@role_required("admin")
def update_student_status(student_id):
    data = request.get_json() or {}
    status = data.get("status", "Active")
    updated = admin_service.user_repo.update_status(student_id, status)
    if not updated:
        return error_response(message=f"Student #{student_id} not found", status_code=404)
    safe = dict(updated)
    safe.pop("password_hash", None)
    return success_response(data=safe, message=f"Student status updated to '{status}'")

@admin_bp.route("/questions", methods=["GET"])
@role_required("admin")
def get_questions():
    questions = question_repo.find_all()
    return success_response(data=questions)

@admin_bp.route("/questions", methods=["POST"])
@role_required("admin")
def create_question():
    data = request.get_json() or {}
    is_valid, msg = validate_question_payload(data)
    if not is_valid:
        return error_response(message=msg, status_code=400)

    # Format question payload
    opt_list = data.get("options", [])
    q_obj = {
        "question_text": data.get("question_text", data.get("question", "")).strip(),
        "option_a": data.get("option_a", opt_list[0] if len(opt_list) > 0 else "").strip(),
        "option_b": data.get("option_b", opt_list[1] if len(opt_list) > 1 else "").strip(),
        "option_c": data.get("option_c", opt_list[2] if len(opt_list) > 2 else "").strip(),
        "option_d": data.get("option_d", opt_list[3] if len(opt_list) > 3 else "").strip(),
        "correct_option": str(data.get("correct_option", data.get("correctIndex", "A"))).upper(),
        "subject_id": data.get("subject_id", 1),
        "subject": data.get("subject", "General CS"),
        "difficulty": data.get("difficulty", "medium").lower(),
        "explanation": data.get("explanation", "").strip()
    }

    created = question_repo.create(q_obj)
    return success_response(data=created, message="Question created successfully", status_code=201)

@admin_bp.route("/questions/<int:question_id>", methods=["PUT"])
@role_required("admin")
def update_question(question_id):
    data = request.get_json() or {}
    updated = question_repo.update(question_id, data)
    if not updated:
        return error_response(message=f"Question #{question_id} not found", status_code=404)
    return success_response(data=updated, message="Question updated successfully")

@admin_bp.route("/questions/<int:question_id>", methods=["DELETE"])
@role_required("admin")
def delete_question(question_id):
    deleted = question_repo.delete(question_id)
    if not deleted:
        return error_response(message=f"Question #{question_id} not found", status_code=404)
    return success_response(message="Question deleted successfully")

@admin_bp.route("/results", methods=["GET"])
@role_required("admin")
def get_all_results():
    results = result_repo.find_all()
    return success_response(data=results)

@admin_bp.route("/jobs", methods=["GET"])
@role_required("admin")
def get_all_jobs():
    jobs = job_service.get_jobs()
    return success_response(data=jobs)

@admin_bp.route("/jobs", methods=["POST"])
@role_required("admin")
def create_job():
    data = request.get_json() or {}
    success, message, created, status_code = job_service.create_job(data)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=created, message=message, status_code=status_code)

@admin_bp.route("/jobs/<int:job_id>", methods=["PUT"])
@role_required("admin")
def update_job(job_id):
    data = request.get_json() or {}
    success, message, updated, status_code = job_service.update_job(job_id, data)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=updated, message=message)

@admin_bp.route("/jobs/<int:job_id>", methods=["DELETE"])
@role_required("admin")
def delete_job(job_id):
    success, message, status_code = job_service.delete_job(job_id)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(message=message)

@admin_bp.route("/applications", methods=["GET"])
@role_required("admin")
def get_all_applications():
    apps = app_service.get_all_applications()
    return success_response(data=apps)

@admin_bp.route("/applications/<int:app_id>/status", methods=["PUT"])
@role_required("admin")
def update_application_status(app_id):
    data = request.get_json() or {}
    status = data.get("status")
    success, message, updated, status_code = app_service.update_application_status(app_id, status)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=updated, message=message)
