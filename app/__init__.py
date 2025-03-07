import threading
import logging
import sys
import redis
import json
from flask import Flask
from app.services.system_monitor import start_monitoring  # ✅ Updated import
from app.services.log_db_handler import store_logs  # ✅ Import log worker
from app.extensions import limiter
from app.security import security_checks, log_requests
from config.log_config import error_logger, main_logger
from app.routes.register_blueprints import register_blueprints  # ✅ Import blueprint registration
from app.utils.log_subscriber import start_log_subscriber  # ✅ Import subscriber

# ✅ Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

logger = logging.getLogger("main")

def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)

    # ✅ Initialize Flask-Limiter
    limiter.init_app(app)

    # ✅ Register API Blueprints
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

    # ✅ Start System Monitoring
    def start_system_monitor():
        if any(thread.name == "SystemMonitorThread" for thread in threading.enumerate()):
            logger.info("⚠️ System Monitoring is already running.")
        else:
            monitoring_thread = threading.Thread(target=start_monitoring, daemon=True, name="SystemMonitorThread")
            monitoring_thread.start()
            logger.info("🚀 System Monitoring Started!")

    start_system_monitor()

    # ✅ Start Log Processing in the Background
    def start_log_processing():
        if any(thread.name == "LogMonitorThread" for thread in threading.enumerate()):
            logger.info("⚠️ Log Monitor is already running.")
        else:
            log_thread = threading.Thread(target=store_logs, daemon=True, name="LogMonitorThread")
            log_thread.start()
            logger.info("📡 Log Monitor Started!")

    start_log_processing()

    # ✅ Start Redis Log Subscriber
    def start_subscriber():
        if any(thread.name == "LogSubscriberThread" for thread in threading.enumerate()):
            logger.info("⚠️ Log Subscriber is already running.")
        else:
            subscriber_thread = threading.Thread(target=start_log_subscriber, daemon=True, name="LogSubscriberThread")
            subscriber_thread.start()
            logger.info("📡 Log Subscriber Started!")

    start_subscriber()

    # ✅ Add a simple home route
    @app.route("/")
    def home():
        log_entry = {"level": "INFO", "message": "Home route accessed!"}
        redis_client.rpush("logninja_logs", json.dumps(log_entry))
        redis_client.publish("logninja_stream", json.dumps(log_entry))
        return "LogNinja is running!"

    return app
