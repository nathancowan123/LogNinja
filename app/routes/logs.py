import redis
import sqlite3
import json
from flask import Blueprint, jsonify, request

# ✅ Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/", methods=["GET"])
def get_logs():
    """Fetch latest logs from SQLite for long-term storage."""
    limit = request.args.get("limit", 10)

    try:
        limit = int(limit)  # Ensure limit is an integer
    except ValueError:
        return jsonify({"error": "Invalid limit parameter. Must be an integer."}), 400

    conn = sqlite3.connect("db/logninja.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, level, message FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    logs = [{"timestamp": row[0], "level": row[1], "message": row[2]} for row in cursor.fetchall()]
    conn.close()

    return jsonify({"logs": logs})  # ✅ Ensure JSON response
