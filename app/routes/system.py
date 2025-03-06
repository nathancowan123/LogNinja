import redis
import json
from flask import Blueprint, jsonify

# ✅ Redis Connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

system_bp = Blueprint("system", __name__)

@system_bp.route("/status", methods=["GET"])
def get_system_status():
    """Fetch latest system status logs from Redis."""
    system_logs = redis_client.lrange("logninja_logs", -5, -1)

    # ✅ Ensure valid JSON response
    if not system_logs:
        return jsonify({"system_status": []})

    try:
        return jsonify({"system_status": [json.loads(log) for log in system_logs]})
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid log data in Redis"}), 500
