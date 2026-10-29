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

@test_bp.route("/<test_id>", methods=["GET"])
def get_test_detail(test_id):
    test = test_service.get_test_by_id(test_id)
    if not test:
        return error_response(message=f"Test #{test_id} not found", status_code=404)
    return success_response(data=test)

@test_bp.route("/<test_id>/practice", methods=["GET", "POST"])
def get_practice_questions(test_id):
    payload = request.get_json(silent=True) or {}
    difficulty = payload.get("difficulty") or request.args.get("difficulty")
    length = payload.get("length") or request.args.get("length")
    if length is not None:
        try:
            length = int(length)
        except (ValueError, TypeError):
            length = None

    success, message, data, status_code = test_service.get_practice_questions(
        test_id, difficulty=difficulty, length=length
    )
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=data, message=message, status_code=status_code)

@test_bp.route("/<test_id>/start", methods=["POST"])
@token_required
def start_test(test_id):
    user_id = g.current_user.get("id")
    payload = request.get_json(silent=True) or {}
    difficulty = payload.get("difficulty") or request.args.get("difficulty")
    length = payload.get("length") or request.args.get("length")
    if length is not None:
        try:
            length = int(length)
        except (ValueError, TypeError):
            length = None

    success, message, data, status_code = test_service.start_test(
        test_id, user_id=user_id, difficulty=difficulty, length=length
    )
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=data, message=message, status_code=status_code)

@test_bp.route("/<test_id>/security-event", methods=["POST"])
@token_required
def log_security_event(test_id):
    user_id = g.current_user.get("id")
    payload = request.get_json() or {}
    success, message, data, status_code = test_service.log_security_event(user_id, test_id, payload)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=data, message=message, status_code=status_code)

@test_bp.route("/attempts/<attempt_id>", methods=["GET"])
@token_required
def get_attempt(attempt_id):
    user_id = g.current_user.get("id")
    role = g.current_user.get("role", "student")
    success, message, data, status_code = test_service.get_attempt_details(attempt_id, user_id=user_id, role=role)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=data, message=message, status_code=status_code)

@test_bp.route("/<test_id>/submit", methods=["POST"])
@token_required
def submit_test(test_id):
    user_id = g.current_user.get("id")
    payload = request.get_json() or {}

    success, message, result, status_code = test_service.submit_test(user_id, test_id, payload)
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=result, message=message, status_code=status_code)
