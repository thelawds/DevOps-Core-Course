import os
import sys
import time
import socket
import platform
import datetime
import logging
from flask import Flask, jsonify, request

# Configuration from environment variables
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# Service start time for uptime calculation
START_TIME = time.time()

# Setup logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def get_uptime_seconds():
    """Calculate service uptime in seconds."""
    return int(time.time() - START_TIME)


def format_uptime_human(seconds):
    """Format uptime in human-readable format."""
    if seconds < 60:
        return f"{seconds} seconds"

    minutes = seconds // 60
    seconds %= 60

    if minutes < 60:
        minute_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
        second_str = f"{seconds} second{'s' if seconds != 1 else ''}"
        return f"{minute_str}, {second_str}"

    hours = minutes // 60
    minutes %= 60

    if hours < 24:
        hour_str = f"{hours} hour{'s' if hours != 1 else ''}"
        minute_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
        return f"{hour_str}, {minute_str}"

    days = hours // 24
    hours %= 24

    day_str = f"{days} day{'s' if days != 1 else ''}"
    hour_str = f"{hours} hour{'s' if hours != 1 else ''}"
    return f"{day_str}, {hour_str}"


def get_system_info():
    """Collect system information."""
    system_platform = platform.system()

    # Platform version detection
    if system_platform == "Linux":
        try:
            import distro
            platform_version = f"{distro.name()} {distro.version()}"
        except ImportError:
            platform_version = platform.version()
    elif system_platform == "Darwin":  # macOS
        platform_version = platform.mac_ver()[0]
    elif system_platform == "Windows":
        platform_version = platform.win32_ver()[0]
    else:
        platform_version = platform.version()

    # CPU count
    try:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        cpu_count = 1

    return {
        "hostname": socket.gethostname(),
        "platform": system_platform,
        "platform_version": platform_version,
        "architecture": platform.machine(),
        "cpu_count": cpu_count,
        "python_version": platform.python_version()
    }


def get_current_timestamp():
    """Get current UTC time in ISO format."""
    return datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'


def log_request_info():
    """Log request information."""
    logger.debug(
        f"Request: {request.method} {request.path} "
        f"from {request.remote_addr} "
        f"User-Agent: {request.user_agent}"
    )


@app.route('/', methods=['GET'])
def service_info():
    """Return service and system information."""
    log_request_info()
    uptime_seconds = get_uptime_seconds()

    response = {
        "service": {
            "name": "devops-info-service",
            "version": "1.0.0",
            "description": "DevOps course info service",
            "framework": "Flask"
        },
        "system": get_system_info(),
        "runtime": {
            "uptime_seconds": uptime_seconds,
            "uptime_human": format_uptime_human(uptime_seconds),
            "current_time": get_current_timestamp(),
            "timezone": "UTC"
        },
        "request": {
            "client_ip": request.remote_addr,
            "user_agent": request.user_agent.string if request.user_agent else "Unknown",
            "method": request.method,
            "path": request.path
        },
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Service information"},
            {"path": "/health", "method": "GET", "description": "Health check"}
        ]
    }

    logger.info(f"Served main endpoint, uptime: {uptime_seconds}s")
    return jsonify(response)


@app.route('/health', methods=['GET'])
def health_check():
    """Return health status of the service."""
    log_request_info()
    uptime_seconds = get_uptime_seconds()

    response = {
        "status": "healthy",
        "timestamp": get_current_timestamp(),
        "uptime_seconds": uptime_seconds
    }

    logger.debug(f"Health check - uptime: {uptime_seconds}s")
    return jsonify(response)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 Not Found: {request.method} {request.path}")
    return jsonify({
        'error': 'Not Found',
        'message': 'Endpoint does not exist'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    logger.warning(
        f"405 Method Not Allowed: {request.method} {request.path}"
    )
    return jsonify({
        'error': 'Method Not Allowed',
        'message': f'{request.method} method is not allowed for this endpoint'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 Internal Server Error: {str(error)}", exc_info=True)
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


@app.before_request
def before_request():
    """Log before processing each request."""
    logger.debug(f"Starting request: {request.method} {request.path}")


@app.after_request
def after_request(response):
    """Log after processing each request."""
    logger.debug(f"Completed request: {request.method} {request.path} - Status: {response.status_code}")
    return response


if __name__ == '__main__':
    logger.info(f"Starting DevOps Info Service on {HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info("Available endpoints: GET /, GET /health")

    try:
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except OSError as e:
        logger.error(f"Failed to start service: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
        sys.exit(0)