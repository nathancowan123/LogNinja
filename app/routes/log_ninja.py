import time
from flask import Blueprint, jsonify
from app.services.ninja import log_manager

LogKillingNinja_bp = Blueprint("LogKillingNinja", __name__)

@LogKillingNinja_bp.route("/delete_logs", methods=["DELETE"])
def delete_logs():
    """🗑️ Manually delete logs ≥ 100MB."""
    deleted_files = log_manager.delete_large_logs()

    return jsonify({
        "message": "✅ Manual log cleanup completed.",
        "deleted_files": deleted_files if deleted_files else "No files needed slaying."
    })
