from flask import jsonify

def success_response(data=None, message="Operation successful", status_code=200):
    """
    Standardized API Success Response Schema
    """
    response_payload = {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(response_payload), status_code

def error_response(message="Something went wrong", error=None, status_code=400):
    """
    Standardized API Error Response Schema
    """
    response_payload = {
        "success": False,
        "message": message,
        "error": error if error is not None else {}
    }
    return jsonify(response_payload), status_code
