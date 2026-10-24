from flask import Blueprint, request, g
from backend.services.test_service import TestService
from backend.utils.responses import success_response, error_response
from backend.utils.decorators import token_required

test_bp = Blueprint("test_bp", __name__, url_prefix="/api/tests")
test_service = TestService()

@test_bp.route("", methods=["GET"])
def get_tests():
    subject = request.args.get("subject")
    difficulty = request.args.get("difficulty")
    tests = test_service.get_tests(subject=subject, difficulty=difficulty)
    return success_response(data=tests)

@test_bp.route("/<int:test_id>", methods=["GET"])
def get_test_detail(test_id):
    test = test_service.get_test_by_id(test_id)
    if not test:
        return error_response(message=f"Test #{test_id} not found", status_code=404)
    return success_response(data=test)

@test_bp.route("/<int:test_id>/start", methods=["POST"])
@token_required
def start_test(test_id):
    success, message, payload, status_code = test_service.start_test(test_id)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=payload, message=message, status_code=status_code)

@test_bp.route("/<int:test_id>/submit", methods=["POST"])
@token_required
def submit_test(test_id):
    user_id = g.current_user.get("id")
    payload = request.get_json() or {}

    success, message, result, status_code = test_service.submit_test(user_id, test_id, payload)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=result, message=message, status_code=status_code)
