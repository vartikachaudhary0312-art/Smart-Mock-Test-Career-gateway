import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present in backend/ or project root
backend_env = Path(__file__).resolve().parent / ".env"
root_env = Path(__file__).resolve().parent.parent / ".env"
if backend_env.exists():
    load_dotenv(dotenv_path=backend_env)
elif root_env.exists():
    load_dotenv(dotenv_path=root_env)

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-smart-mock-test-2026")
    CORS_ORIGINS = ["*"]
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024)) # 5MB limit
    JSON_SORT_KEYS = False

    # Single Authorized Administrator
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "vartikachaudhary0312@gmail.com").strip().lower()
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "").strip()

    # SMTP settings
    MAIL_SERVER = os.getenv("MAIL_SERVER", "")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "")
    OTP_TTL_SECONDS = int(os.getenv("OTP_TTL_SECONDS", 300))
    OTP_RESEND_COOLDOWN_SECONDS = int(os.getenv("OTP_RESEND_COOLDOWN_SECONDS", 30))

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    CORS_ORIGINS = ["*"]

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test-secret-key"
    CORS_ORIGINS = ["*"]
    ADMIN_EMAIL = "vartikachaudhary0312@gmail.com"
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Vartika@123").strip()

class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"
    CORS_ORIGINS = [origin.strip() for origin in os.getenv(
        "CORS_ORIGINS",
        "http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:5000,http://localhost:5000"
    ).split(",")]

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
