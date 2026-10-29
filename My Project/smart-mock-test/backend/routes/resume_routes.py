from flask import Blueprint, request, current_app, g
from backend.services.resume_service import ResumeService
from backend.utils.responses import success_response, error_response
from backend.utils.decorators import token_required

resume_bp = Blueprint("resume_bp", __name__, url_prefix="/api/resume")

@resume_bp.route("/upload", methods=["POST"])
@token_required
def upload_resume():
    if "file" not in request.files and "resume" not in request.files:
        return error_response(message="No resume file payload attached.", status_code=400)

    file_obj = request.files.get("file") or request.files.get("resume")
    resume_service = ResumeService(upload_folder=current_app.config.get("UPLOAD_FOLDER", "uploads"))

    user_id = g.current_user.get("id")
    success, message, analysis, status_code = resume_service.process_resume_upload(file_obj, user_id=user_id)
    if not success:
        return error_response(message=message, status_code=status_code)

    return success_response(data=analysis, message=message, status_code=status_code)

@resume_bp.route("/latest", methods=["GET"])
@token_required
def get_latest_resume():
    user_id = g.current_user.get("id")
    resume_service = ResumeService(upload_folder=current_app.config.get("UPLOAD_FOLDER", "uploads"))
    analysis = resume_service.get_user_resume_analysis(user_id)
    if not analysis:
        return error_response(message="No resume uploaded yet.", status_code=404)
    return success_response(data=analysis)

@resume_bp.route("", methods=["DELETE"])
@token_required
def delete_resume():
    user_id = g.current_user.get("id")
    resume_service = ResumeService(upload_folder=current_app.config.get("UPLOAD_FOLDER", "uploads"))
    resume_service.delete_user_resume(user_id)
    return success_response(message="Resume removed successfully")
