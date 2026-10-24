from flask import Blueprint, request, current_app, g
from backend.services.auth_service import AuthService
from backend.services.email_otp_service import (
    EmailOTPService,
    OTPConfigurationError,
    OTPDeliveryError,
    OTPResendTooSoon,
    OTPVerificationError
)
from backend.utils.responses import success_response, error_response
from backend.utils.decorators import token_required
from backend.utils.validators import validate_email

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")
auth_service = AuthService()
email_otp_service = EmailOTPService()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    success, message, result, status_code = auth_service.register_user(data, current_app.config["SECRET_KEY"])
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=result, message=message, status_code=status_code)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    requested_role = (data.get("role") or data.get("requested_role") or "student").strip().lower()

    success, message, result, status_code = auth_service.login_user(
        email, password, current_app.config["SECRET_KEY"], requested_role=requested_role
    )
    if not success:
        return error_response(message=message, status_code=status_code)
    return success_response(data=result, message=message, status_code=status_code)

@auth_bp.route("/test-otp/send", methods=["POST"])
def send_test_otp():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "") if isinstance(data, dict) else ""
    email = email.strip().lower() if isinstance(email, str) else ""
    if not validate_email(email):
        return error_response(message="A valid registration email is required.", status_code=400)

    try:
        delivery = email_otp_service.send(email, current_app.config)
    except OTPConfigurationError as error:
        return error_response(message=str(error), status_code=503)
    except OTPResendTooSoon as error:
        return error_response(
            message=str(error),
            error={"retry_after_seconds": error.retry_after_seconds},
            status_code=429
        )
    except OTPDeliveryError as error:
        return error_response(message=str(error), status_code=502)

    return success_response(
        data=delivery,
        message="A verification code was sent to your registration email."
    )

@auth_bp.route("/test-otp/verify", methods=["POST"])
def verify_test_otp():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "") if isinstance(data, dict) else ""
    code = data.get("code", "") if isinstance(data, dict) else ""
    email = email.strip().lower() if isinstance(email, str) else ""
    if not validate_email(email):
        return error_response(message="A valid registration email is required.", status_code=400)

    try:
        email_otp_service.verify(email, code)
    except OTPVerificationError as error:
        return error_response(message=str(error), status_code=400)

    return success_response(data={"verified": True}, message="Email verification successful.")

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return success_response(message="Logged out successfully", data={})

@auth_bp.route("/me", methods=["GET"])
@token_required
def get_me():
    user_id = g.current_user.get("id")
    profile = auth_service.get_current_user_profile(user_id)
    if not profile:
        return error_response(message="User not found", status_code=404)
    return success_response(data={"user": profile})
