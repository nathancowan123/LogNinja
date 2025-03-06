import redis
import json
from flask import Blueprint, jsonify, request

# ✅ Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts", methods=["POST"])
def trigger_alert():
    """Manually trigger an alert."""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing message field"}), 400

    alert_entry = {"level": "ALERT", "message": data["message"]}
    redis_client.rpush("logninja_alerts", json.dumps(alert_entry))  # Store alert in Redis
    redis_client.publish("logninja_alert_stream", json.dumps(alert_entry))  # Publish alert to listeners

    return jsonify({"status": "Alert triggered!"})
