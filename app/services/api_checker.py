import logging
from app.utils.logger import log_message

logger = logging.getLogger("LogNinja")

# ✅ Keep track of previous API usage to prevent duplicate logs
_api_usage_history = {}

def check_api_rate_limits(api_name, max_requests, used_requests):
    """
    Checks API usage and logs warnings if rate limit is approaching.
    Prevents duplicate logs if the API is in the same usage range as last check.
    """
    if max_requests == 0:
        log_message(f"❌ Invalid max request count for {api_name}.", "error")
        return 0

    percentage_used = (used_requests / max_requests) * 100

    # ✅ Prevent duplicate logs (log only when crossing thresholds)
    prev_usage = _api_usage_history.get(api_name, 0)
    _api_usage_history[api_name] = percentage_used  # Store latest usage

    if 80 <= percentage_used < 90 and prev_usage < 80:
        log_message(f"⚠️ {api_name} API is approaching its rate limit! ({percentage_used:.2f}% used)", "warning")

    elif percentage_used >= 90 and prev_usage < 90:
        log_message(f"🚨 CRITICAL: {api_name} API limit nearly exhausted! ({percentage_used:.2f}% used)", "error")

    return percentage_used  # Return the percentage used for monitoring
