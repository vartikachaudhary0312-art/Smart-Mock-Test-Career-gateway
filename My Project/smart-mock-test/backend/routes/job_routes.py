from flask import Blueprint, request, g
from backend.services.job_service import JobService
from backend.services.application_service import ApplicationService
from backend.utils.responses import success_response, error_response
from backend.utils.decorators import token_required, role_required

job_bp = Blueprint("job_bp", __name__, url_prefix="/api/jobs")
job_service = JobService()
app_service = ApplicationService()

@job_bp.route("", methods=["GET"])
def get_jobs():
    company = request.args.get("company")
    location = request.args.get("location")
    skills = request.args.get("skills")
    job_type = request.args.get("job_type") or request.args.get("type")

    jobs = job_service.get_jobs(company=company, location=location, skills=skills, job_type=job_type)
    return success_response(data=jobs)

@job_bp.route("/<int:job_id>", methods=["GET"])
def get_job_detail(job_id):
    job = job_service.get_job_by_id(job_id)
    if not job:
        return error_response(message=f"Job posting #{job_id} not found", status_code=404)
    return success_response(data=job)

@job_bp.route("/<int:job_id>/apply", methods=["POST"])
@role_required("student")
def apply_job(job_id):
    student_id = g.current_user.get("id")
    success, message, created_app, status_code = app_service.apply_for_job(student_id, job_id)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=created_app, message=message, status_code=status_code)
