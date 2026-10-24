from flask import Blueprint, g
from backend.utils.responses import success_response
from backend.utils.decorators import token_required

notification_bp = Blueprint("notification_bp", __name__, url_prefix="/api/notifications")

@notification_bp.route("", methods=["GET"])
@token_required
def get_notifications():
    mock_notifs = [
        {
            "id": 1,
            "title": "Mock Test Completed",
            "message": "You scored 80% on Java Programming (Medium). Great job!",
            "time": "2 hours ago",
            "read": False
        },
        {
            "id": 2,
            "title": "New Career Match",
            "message": "CloudScale Systems posted a job matching your Python skills.",
            "time": "1 day ago",
            "read": True
        }
    ]
    return success_response(data=mock_notifs)
