from flask import Blueprint, g
from backend.services.application_service import ApplicationService
from backend.utils.responses import success_response
from backend.utils.decorators import token_required

application_bp = Blueprint("application_bp", __name__, url_prefix="/api/applications")
app_service = ApplicationService()

@application_bp.route("", methods=["GET"])
@token_required
def get_applications():
    user_id = g.current_user.get("id")
    role = g.current_user.get("role")

    if role == "admin":
        apps = app_service.get_all_applications()
    else:
        apps = app_service.get_student_applications(user_id)

    return success_response(data=apps)
