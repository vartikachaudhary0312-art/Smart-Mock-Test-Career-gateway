import os
from flask import Flask, jsonify
from backend.config import config_by_name
from backend.extensions import cors
from backend.utils.responses import error_response, success_response

def create_app(config_name=None) -> Flask:
    """
    Flask Application Factory for Smart Mock Test & Career Gateway API.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    # Initialize CORS
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Root & Health Check Endpoints
    @app.route("/", methods=["GET"])
    def index():
        return success_response(
            data={
                "service": "Smart Mock Test and Career Gateway API",
                "version": "1.0.0",
                "health": "/api/health"
            },
            message="Welcome to Smart Mock Test & Career Gateway Flask API. Access /api/health for system status.",
            status_code=200
        )

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return success_response(
            data={
                "service": "backend",
                "status": "healthy"
            },
            message="Smart Mock Test API is running",
            status_code=200
        )

    # Register Blueprints
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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
