import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    DEBUG = os.getenv("DEBUG", True)
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    FILE_SIZE_LIMIT = int(os.getenv("FILE_SIZE_LIMIT", 100 * 1024 * 1024))  # 100MB
    INACTIVITY_THRESHOLD = int(os.getenv("INACTIVITY_THRESHOLD", 180))  # 3 minutes

    # ✅ Load LogNinja API Key from .env
    LOGNINJA_API_KEY = os.getenv("LOGNINJA_API_KEY", "default-api-key")  # Default for safety
