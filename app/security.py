import logging
from flask import request, abort
from collections import defaultdict

logger = logging.getLogger("LogNinja")

KNOWN_BOTS = ["Googlebot", "Bingbot", "Slurp", "DuckDuckBot", "Baiduspider"]
BLOCKED_IPS = set()
FAILED_ATTEMPTS = defaultdict(int)

def security_checks():
    """Blocks bots and excessive failed requests."""
    ip = request.remote_addr

    if ip in BLOCKED_IPS:
        logger.warning(f"🚫 Blocked IP: {ip}")
        abort(403)

    if detect_spider():
        abort(403)

    if FAILED_ATTEMPTS[ip] > 5:
        logger.warning(f"🚫 Auto-banning IP: {ip} due to excessive failed requests.")
        BLOCKED_IPS.add(ip)
        abort(403)

def log_requests(response):
    """Logs all requests for monitoring."""
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')

    if response.status_code == 403:
        logger.warning(f"🚫 Blocked: IP={ip}, UA={user_agent}")
    else:
        logger.info(f"✅ Request: {request.method} {request.path} from {ip}")

    return response

def detect_spider():
    """Detects and logs bot activity."""
    user_agent = request.headers.get("User-Agent", "").lower()
    remote_ip = request.remote_addr

    for bot in KNOWN_BOTS:
        if bot.lower() in user_agent:
            logger.warning(f"🐞 Detected bot: {user_agent} from IP {remote_ip}")
            BLOCKED_IPS.add(remote_ip)
            return True
    return False
