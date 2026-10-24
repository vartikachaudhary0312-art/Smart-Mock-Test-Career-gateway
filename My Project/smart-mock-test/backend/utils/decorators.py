from functools import wraps
from flask import request, current_app, g
from backend.utils.responses import error_response
from backend.utils.security import verify_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
            elif len(parts) == 1:
                token = parts[0]
        
        if not token:
            token = request.args.get("token") or request.cookies.get("token")

        if not token:
            return error_response(
                message="Authentication required. Missing Bearer token.",
                error={"code": "UNAUTHORIZED"},
                status_code=401
            )

        payload = verify_token(token, current_app.config["SECRET_KEY"])
        if not payload:
            return error_response(
                message="Invalid or expired authentication token.",
                error={"code": "INVALID_TOKEN"},
                status_code=401
            )

        g.current_user = payload
        return f(*args, **kwargs)

    return decorated

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            user_role = g.current_user.get("role")
            if user_role not in allowed_roles:
                return error_response(
                    message=f"Access denied. Requires one of roles: {list(allowed_roles)}.",
                    error={"code": "FORBIDDEN", "user_role": user_role},
                    status_code=403
                )
            return f(*args, **kwargs)
        return decorated
    return decorator
