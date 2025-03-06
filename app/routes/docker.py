import os
import redis
import json
import subprocess
from flask import Blueprint, jsonify

# ✅ Redis Connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

docker_bp = Blueprint("docker", __name__)

@docker_bp.route("/status", methods=["GET"])
def get_docker_status():
    """Fetch running Docker containers and return JSON response."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}} {{.Status}}"],
            stdout=subprocess.PIPE, text=True, check=True
        )
        containers = [line.split(" ", 1) for line in result.stdout.strip().split("\n") if line]
        
        # ✅ Format the output as a list of dictionaries
        formatted_containers = [{"name": container[0], "status": container[1]} for container in containers]

        # ✅ Store Docker status in Redis for quick access
        redis_client.set("logninja_docker", json.dumps(formatted_containers))

        return jsonify({"docker_status": formatted_containers})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to retrieve Docker status: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
