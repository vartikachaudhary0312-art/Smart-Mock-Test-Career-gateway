from flask import Blueprint, request, current_app
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
    resume_service = ResumeService(upload_folder=current_app.config["UPLOAD_FOLDER"])

    success, message, analysis, status_code = resume_service.process_resume_upload(file_obj)
    if not success:
        return error_response(message=message, status_code=status_code)

    return success_response(data=analysis, message=message, status_code=status_code)
