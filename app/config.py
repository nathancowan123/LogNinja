import os

class Config:
    """Base configuration class."""
    DEBUG = os.getenv("DEBUG", True)
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    FILE_SIZE_LIMIT = int(os.getenv("FILE_SIZE_LIMIT", 100 * 1024 * 1024))  # 100MB
    INACTIVITY_THRESHOLD = int(os.getenv("INACTIVITY_THRESHOLD", 180))  # 3 minutes
    