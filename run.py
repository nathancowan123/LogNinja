from app import create_app
from app.config import Config  # Import the config with API key
from logninja_core import LogNinja

# ✅ Initialize LogNinja with API key
log_ninja = LogNinja(api_key=Config.LOGNINJA_API_KEY)
log_ninja.log_event("LogNinja initialized with API key!", severity="info")

# ✅ Create the Flask app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8100, debug=True)
