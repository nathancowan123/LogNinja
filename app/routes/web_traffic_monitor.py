from flask import Blueprint, jsonify, request
from app.extensions import limiter  # ✅ Import limiter properly
import logging

# ✅ Set up logging
logger = logging.getLogger("LogNinja")

# ✅ Create Blueprint for Web Traffic Monitoring
web_traffic_bp = Blueprint("web_traffic_monitor", __name__)

# ✅ Track HTTP 500 Errors
@web_traffic_bp.app_errorhandler(500)
def handle_500_error(e):
    logger.error(f"❌ HTTP 500 Error: {str(e)} - Path: {request.path} - IP: {request.remote_addr}")
    return jsonify({"error": "Internal Server Error"}), 500

# ✅ Log Requests for Traffic Monitoring
@web_traffic_bp.before_request
def log_request():
    logger.info(f"📡 Request: {request.method} {request.path} - IP: {request.remote_addr}")

# ✅ Add a Rate-Limited Test Route
@web_traffic_bp.route("/test", methods=["GET"])
@limiter.limit("10 per second")  # ✅ Now properly using imported limiter
def test_route():
    return jsonify({"message": "Rate limit test successful"}), 200

# ✅ Trigger a 500 Error for Testing
@web_traffic_bp.route("/trigger-500", methods=["GET"])
def trigger_error():
    raise Exception("Testing HTTP 500 logging")
