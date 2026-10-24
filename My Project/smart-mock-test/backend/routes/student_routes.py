from flask import Blueprint, request, g
from backend.services.student_service import StudentService
from backend.utils.responses import success_response, error_response
from backend.utils.decorators import token_required, role_required

student_bp = Blueprint("student_bp", __name__, url_prefix="/api/student")
student_service = StudentService()

@student_bp.route("/profile", methods=["GET"])
@token_required
def get_profile():
    user_id = g.current_user.get("id")
    profile = student_service.get_profile(user_id)
    if not profile:
        return error_response(message="Student profile not found", status_code=404)
    return success_response(data={"profile": profile})

@student_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile():
    user_id = g.current_user.get("id")
    data = request.get_json() or {}
    success, message, updated = student_service.update_profile(user_id, data)
    if not success:
        return error_response(message=message, status_code=400)
    return success_response(data={"profile": updated}, message=message)
