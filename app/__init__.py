from flask import Flask
from app.routes.blueprints import register_blueprints
import threading
from app.services.ninja import log_manager

def create_app():
    app = Flask(__name__)

    # Register all blueprints
    register_blueprints(app)

    # Start background log monitoring
    thread = threading.Thread(target=log_manager.monitor_logs, daemon=True)
    thread.start()

    return app
