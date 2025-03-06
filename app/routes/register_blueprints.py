from flask import Blueprint
from app.routes.logs import logs_bp
from app.routes.system import system_bp
from app.routes.docker import docker_bp
from app.routes.alerts import alerts_bp

def register_blueprints(app):
    """Registers all API blueprints to the Flask app."""
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    # ✅ Register each service's API under "/api"
    api_bp.register_blueprint(logs_bp, url_prefix="/logs")
    api_bp.register_blueprint(system_bp, url_prefix="/system")
    api_bp.register_blueprint(docker_bp, url_prefix="/docker")
    api_bp.register_blueprint(alerts_bp, url_prefix="/alerts")

    # ✅ Attach "/api" blueprint to the main app
    app.register_blueprint(api_bp)
