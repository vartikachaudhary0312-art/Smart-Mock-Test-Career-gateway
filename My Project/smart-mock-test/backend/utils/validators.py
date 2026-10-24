import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^\+?[0-9]{10,15}$'

def validate_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(EMAIL_REGEX, email.strip()))

def validate_phone(phone: str) -> bool:
    if not phone or not isinstance(phone, str):
        return False
    clean_phone = phone.strip().replace(" ", "").replace("-", "")
    return bool(re.match(PHONE_REGEX, clean_phone))

def validate_password(password: str) -> tuple[bool, str]:
    if not password or not isinstance(password, str):
        return False, "Password is required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""

def validate_registration_payload(data: dict) -> tuple[bool, str]:
    if not data or not isinstance(data, dict):
        return False, "Request body must be valid JSON."

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not name:
        return False, "Full name is required."
    if not validate_email(email):
        return False, "Valid email address is required."
    
    is_valid_pwd, msg = validate_password(password)
    if not is_valid_pwd:
        return False, msg

    confirm_password = data.get("confirm_password", data.get("confirmPassword", "")).strip()
    if confirm_password and confirm_password != password:
        return False, "Passwords do not match."

    return True, ""

def validate_question_payload(data: dict) -> tuple[bool, str]:
    if not data or not isinstance(data, dict):
        return False, "Request payload must be a JSON object."

    q_text = data.get("question_text", data.get("question", "")).strip()
    if not q_text:
        return False, "Question text is required."

    options = [
        data.get("option_a", data.get("options", [""])[0] if len(data.get("options", [])) > 0 else ""),
        data.get("option_b", data.get("options", ["", ""])[1] if len(data.get("options", [])) > 1 else ""),
        data.get("option_c", data.get("options", ["", "", ""])[2] if len(data.get("options", [])) > 2 else ""),
        data.get("option_d", data.get("options", ["", "", "", ""])[3] if len(data.get("options", [])) > 3 else "")
    ]

    for idx, opt in enumerate(options):
        if not opt or not str(opt).strip():
            return False, f"Option {chr(65 + idx)} is required."

    correct_option = str(data.get("correct_option", data.get("correctIndex", ""))).strip()
    valid_choices = ["A", "B", "C", "D", "0", "1", "2", "3"]
    if correct_option not in valid_choices:
        return False, "Correct option must be A, B, C, or D."

    return True, ""
