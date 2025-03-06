import redis
import json
from flask import Blueprint, jsonify, request

# ✅ Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/logs", methods=["GET"])
def get_logs():
    """Fetch latest logs from Redis."""
    limit = request.args.get("limit", 10)  # Get limit from request
    try:
        limit = int(limit)  # Ensure limit is an integer
    except ValueError:
        return jsonify({"error": "Invalid limit parameter. Must be an integer."}), 400

    logs = redis_client.lrange("logninja_logs", -limit, -1)  # Get last 'limit' logs
    formatted_logs = [json.loads(log) for log in logs]  # Ensure proper JSON

    return jsonify({"logs": formatted_logs})  # ✅ Always return a JSON object
