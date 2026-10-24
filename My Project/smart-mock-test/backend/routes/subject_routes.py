from flask import Blueprint
from backend.services.test_service import TestService
from backend.utils.responses import success_response

subject_bp = Blueprint("subject_bp", __name__, url_prefix="/api/subjects")
test_service = TestService()

@subject_bp.route("", methods=["GET"])
def get_subjects():
    subjects = test_service.get_all_subjects()
    return success_response(data=subjects)
