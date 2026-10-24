import time
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

def hash_password(password: str) -> str:
    """Hash plain-text password using Werkzeug's default pbkdf2 algorithm."""
    return generate_password_hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    """Verify plain-text password against stored Werkzeug hash."""
    return check_password_hash(password_hash, password)

def generate_token(user_data: dict, secret_key: str, expires_in: int = 86400) -> str:
    """
    Generate a signed authentication token containing minimal user payload.
    """
    serializer = URLSafeTimedSerializer(secret_key)
    payload = {
        "id": user_data.get("id"),
        "email": user_data.get("email"),
        "role": user_data.get("role"),
        "iat": int(time.time())
    }
    return serializer.dumps(payload, salt="auth-salt")

def verify_token(token: str, secret_key: str, max_age: int = 86400) -> dict | None:
    """
    Verify and decode a signed authentication token.
    """
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        payload = serializer.loads(token, salt="auth-salt", max_age=max_age)
        return payload
    except (BadSignature, SignatureExpired):
        return None
