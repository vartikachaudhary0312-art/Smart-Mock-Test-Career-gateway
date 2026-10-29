"""
Smart Mock Test & Career Gateway — Application Entry Point
Usage:
    python run.py
"""
import sys
from pathlib import Path

# Ensure project directory is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app import create_app

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

