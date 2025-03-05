import threading
import logging
import os
import sys
from flask import Flask
from app.routes.blueprints import register_blueprints
from app.services.system_monitor import run_system_monitor
from app.services.log_db_handler import start_log_monitor  # ✅ Import log monitor
from app.extensions import limiter
from app.security import security_checks, log_requests
from config.log_config import error_logger, ratelimit_logger, unauthorized_logger, main_logger

logger = logging.getLogger("main")

def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)

    # ✅ Initialize Flask-Limiter
    limiter.init_app(app)

    # ✅ Register all blueprints (API routes) centrally
    register_blueprints(app)

    # ✅ Security Middleware
    app.before_request(security_checks)
    app.after_request(log_requests)

    # ✅ Attach Flask logs to Gunicorn logs
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_error_logger.handlers

    # ✅ Also attach Flask logs to LogNinja's main logger
    for handler in main_logger.handlers:
        app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)

    # ✅ Start System Monitoring (Runs Once)
    def start_monitoring():
        if any(thread.name == "SystemMonitorThread" for thread in threading.enumerate()):
            logger.info("⚠️ System Monitoring is already running.")
        else:
            monitoring_thread = threading.Thread(target=run_system_monitor, daemon=True, name="SystemMonitorThread")
            monitoring_thread.start()
            logger.info("🚀 System Monitoring Started!")

    start_monitoring()

    # ✅ Start Log Monitoring (Runs Once)
    def start_log_processing():
        if any(thread.name == "LogMonitorThread" for thread in threading.enumerate()):
            logger.info("⚠️ Log Monitor is already running.")
        else:
            log_thread = threading.Thread(target=start_log_monitor, daemon=True, name="LogMonitorThread")
            log_thread.start()
            logger.info("📡 Log Monitor Started!")

    start_log_processing()

    return app
