from flask import Flask
from app.routes.log_ninja import LogKillingNinja_bp

def register_blueprints(app: Flask):
    """Registers all Flask blueprints to the app."""
    app.register_blueprint(LogKillingNinja_bp, url_prefix="/ninja")
