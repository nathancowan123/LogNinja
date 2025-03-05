from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ✅ Define Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per minute", "5000 per hour"],
    storage_uri="memory://",  # Use Redis in production
)
