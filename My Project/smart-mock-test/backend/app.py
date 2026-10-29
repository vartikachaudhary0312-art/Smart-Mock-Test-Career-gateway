import os
import sys
from pathlib import Path

# Ensure project root is in sys.path regardless of execution directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, jsonify, send_from_directory
from backend.config import config_by_name
from backend.extensions import cors
from backend.utils.responses import error_response, success_response

def create_app(config_name=None) -> Flask:
    """
    Flask Application Factory for Smart Mock Test & Career Gateway API.
    Serves both the REST API endpoints and the responsive frontend web app.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    frontend_dir = PROJECT_ROOT / "frontend"

    app = Flask(
        __name__,
        static_folder=str(frontend_dir),
        static_url_path=""
    )
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    # Initialize CORS for all origins in development / testing
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": app.config.get("CORS_ORIGINS", ["*"]),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
            }
        }
    )

    # Health Check Endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return success_response(
            data={
                "service": "backend",
                "status": "healthy",
                "version": "1.0.0",
                "admin_email": app.config.get("ADMIN_EMAIL", "vartikachaudhary0312@gmail.com")
            },
            message="Smart Mock Test API is running",
            status_code=200
        )

    # Register API Blueprints
    from backend.routes.auth_routes import auth_bp
    from backend.routes.student_routes import student_bp
    from backend.routes.subject_routes import subject_bp
    from backend.routes.test_routes import test_bp
    from backend.routes.result_routes import result_bp
    from backend.routes.resume_routes import resume_bp
    from backend.routes.job_routes import job_bp
    from backend.routes.application_routes import application_bp
    from backend.routes.notification_routes import notification_bp
    from backend.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(subject_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(admin_bp)

    # Frontend Page Routing
    @app.route("/", methods=["GET"])
    def index():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return send_from_directory(str(frontend_dir), "index.html")
        return success_response(
            data={"service": "backend", "status": "healthy"},
            message="Smart Mock Test & Career Gateway API is running.",
            status_code=200
        )

    @app.route("/<path:filename>", methods=["GET"])
    def serve_frontend(filename):
        # Prevent accessing API paths via static route
        if filename.startswith("api/"):
            return error_response(message="API endpoint not found", status_code=404)

        file_path = frontend_dir / filename
        if file_path.exists() and file_path.is_file():
            return send_from_directory(str(frontend_dir), filename)

        # Check subdirectories like admin/<filename>
        admin_file = frontend_dir / "admin" / filename
        if admin_file.exists() and admin_file.is_file():
            return send_from_directory(str(frontend_dir / "admin"), filename)

        return error_response(message="Page not found", status_code=404)

    # Centralized Error Handlers
    @app.errorhandler(400)
    def bad_request_error(e):
        return error_response(message="Bad Request", error=str(e), status_code=400)

    @app.errorhandler(401)
    def unauthorized_error(e):
        return error_response(message="Unauthorized Access", error=str(e), status_code=401)

    @app.errorhandler(403)
    def forbidden_error(e):
        return error_response(message="Forbidden Access", error=str(e), status_code=403)

    @app.errorhandler(404)
    def not_found_error(e):
        return error_response(message="Requested API Resource Not Found", error=str(e), status_code=404)

    @app.errorhandler(409)
    def conflict_error(e):
        return error_response(message="Resource Conflict", error=str(e), status_code=409)

    @app.errorhandler(422)
    def unprocessable_entity_error(e):
        return error_response(message="Unprocessable Entity Payload", error=str(e), status_code=422)

    @app.errorhandler(500)
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

    return app

if __name__ == "__main__":
    app = create_app("development")
    print("=" * 65)
    print("  🚀 Smart Mock Test & Career Gateway Server running!")
    print("  🌐 Web URL:      http://127.0.0.1:5000")
    print("  🔑 Login Page:   http://127.0.0.1:5000/login.html")
    print("  📝 Register:     http://127.0.0.1:5000/register.html")
    print("  🩺 API Health:   http://127.0.0.1:5000/api/health")
    print("=" * 65)
    app.run(host="0.0.0.0", port=5000, debug=True)
