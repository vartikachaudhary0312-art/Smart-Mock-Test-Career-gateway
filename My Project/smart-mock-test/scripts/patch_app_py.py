with open('My Project/smart-mock-test/backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

old_part = """    @app.errorhandler(500)
    def internal_server_error(e):
        return error_response(message="Internal Server Error", error="An unexpected error occurred on the server.", status_code=500)

    return app"""

new_part = """    @app.errorhandler(500)
    def internal_server_error(e):
        return error_response(message="Internal Server Error", error="An unexpected error occurred on the server.", status_code=500)

    # Safe Admin Provisioning on App Initialization
    try:
        from backend.services.auth_service import AuthService
        auth_service = AuthService()
        admin_email = app.config.get("ADMIN_EMAIL", "vartikachaudhary0312@gmail.com")
        admin_pw = app.config.get("ADMIN_PASSWORD", "")
        if admin_pw:
            auth_service.provision_admin_account(admin_email, admin_pw)
    except Exception as e:
        app.logger.warning(f"Admin provisioning check: {e}")

    return app"""

assert old_part in content_norm, "old_part not found"
content_norm = content_norm.replace(old_part, new_part)

with open('My Project/smart-mock-test/backend/app.py', 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("app.py updated with provisioning hook")

