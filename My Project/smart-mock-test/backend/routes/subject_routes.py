from flask import Blueprint, request
from backend.services.test_service import TestService
from backend.utils.responses import success_response, error_response

subject_bp = Blueprint("subject_bp", __name__, url_prefix="/api/subjects")
test_service = TestService()

@subject_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = test_service.get_all_categories()
    return success_response(data=categories)

@subject_bp.route("/categories/<cat_id>", methods=["GET"])
def get_category_detail(cat_id):
    cat = test_service.get_category_by_id(cat_id)
    if not cat:
        return error_response(message=f"Category '{cat_id}' not found", status_code=404)
    return success_response(data=cat)

@subject_bp.route("", methods=["GET"])
def get_subjects():
    category_id = request.args.get("category_id") or request.args.get("category")
    subjects = test_service.get_all_subjects(category_id=category_id)
    return success_response(data=subjects)

@subject_bp.route("/<subject_id>", methods=["GET"])
def get_subject_detail(subject_id):
    subjects = test_service.get_all_subjects()
    s_id_lower = str(subject_id).strip().lower()
    matched = next((s for s in subjects if str(s.get("id", "")).lower() == s_id_lower or str(s.get("code", "")).lower() == s_id_lower or str(s.get("name", "")).lower() == s_id_lower), None)
    if not matched:
        return error_response(message=f"Topic or subject '{subject_id}' not found", status_code=404)
    return success_response(data=matched)
