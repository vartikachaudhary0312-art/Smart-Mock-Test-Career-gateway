from flask import Blueprint, g
from backend.services.result_service import ResultService
from backend.utils.responses import success_response, error_response
from backend.utils.decorators import token_required

result_bp = Blueprint("result_bp", __name__, url_prefix="/api/results")
result_service = ResultService()

@result_bp.route("", methods=["GET"])
@token_required
def get_user_results():
    user_id = g.current_user.get("id")
    results = result_service.get_user_results(user_id)
    return success_response(data=results)

@result_bp.route("/<int:result_id>", methods=["GET"])
@token_required
def get_result(result_id):
    result = result_service.get_result_by_id(result_id)
    if not result:
        return error_response(message=f"Result #{result_id} not found", status_code=404)
    return success_response(data=result)

@result_bp.route("/<int:result_id>/analysis", methods=["GET"])
@token_required
def get_analysis(result_id):
    success, message, analysis = result_service.get_performance_analysis(result_id)
    if not success:
        return error_response(message=message, status_code=404)
    return success_response(data=analysis, message=message)
