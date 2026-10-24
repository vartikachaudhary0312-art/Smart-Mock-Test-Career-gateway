import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent / "smart-mock-test"
sys.path.insert(0, str(PROJECT_DIR))

from backend.app import create_app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])