import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

class Config:
    LOGNINJA_API_KEY = os.getenv("LOGNINJA_API_KEY", "your-default-api-key")
    DEBUG = True  # Change to False in production
    LOG_FILE = "logs/logninja.log"

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    default_limits=["500 per minute"],  # Increase limit to prevent blocking internal requests
    storage_uri="memory://",  # Avoid persistent storage slowdowns
)

# Load settings
settings = Config()