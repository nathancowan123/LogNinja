from flask import Flask
from app.routes.web_traffic_monitor import web_traffic_bp  # ✅ Import web traffic monitoring blueprint
from app.routes.log_ninja import LogKillingNinja_bp  # ✅ Import LogNinja routes

def register_blueprints(app: Flask):
    """Registers all Flask blueprints to the app."""
    
    # ✅ Check and register web traffic monitoring
    if "web_traffic_monitor" not in app.blueprints:
        app.register_blueprint(web_traffic_bp, url_prefix="/traffic")
    
    # ✅ Check and register Log Ninja routes
    if "log_ninja" not in app.blueprints:
        app.register_blueprint(LogKillingNinja_bp, url_prefix="/ninja")
