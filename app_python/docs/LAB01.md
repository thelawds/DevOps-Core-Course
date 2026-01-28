# Framework selection

Framework of my choice is Flask, because of the following reasons:
- It is lightweight compared to Django
- I have some experience using it in production environments opposing to fastapi

# Flask vs FastAPI vs Django Comparison

| Framework | Simplicity | Performance | Async Support | Best Suited For |
|-----------|------------|-------------|---------------|-----------------|
| **Flask** | Very simple and intuitive | Moderate | Not included | **Small to medium APIs, rapid prototyping, learning** |
| **FastAPI** | Moderate | Excellent | Very good | **Modern REST APIs, microservices, high-performance apps** |
| **Django** | Totally overkill in learning curve for simple projects | Good | Limited | **Full-featured web applications, enterprise projects** |

# Best Practices

## 1. Configuration from environment variables

```python
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
```

It is important, as it allows the code to be easily suited to different environments and allows us to easily apply changes to the project (especially with compiled languages as those changes wouldn't require full rebuild of the project)

## 2. Propper logging

```python
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
```

It is important to keep track of how our application is working and propper logging congfiguration allows us to understand it's state, trace down any problems that may occur and keep track of those.

## 3. Centralized Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found: {request.method} {request.path}")
    return jsonify({
        'error': 'Not Found',
        'message': 'Endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Server Error: {str(error)}", exc_info=True)
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500
```

It is very important to provide clients (probably UI applications) with comprehensive explanations of what went wrong as it not only improves user experience, but also improves our ability to trace the errors and find bugs.

# API Documentation 


### GET `/` - Service Information

**Description:** Returns comprehensive information about the service, system, and current request.

**HTTP Method:** GET

**Response Format:** JSON

**Example Request:**
```bash
curl http://localhost:5000/
```

**Example Response:**
```json
{
  "service": {
    "name": "devops-info-service",
    "version": "1.0.0",
    "description": "DevOps course info service",
    "framework": "Flask"
  },
  "system": {
    "hostname": "my-laptop",
    "platform": "Linux",
    "platform_version": "Ubuntu 24.04",
    "architecture": "x86_64",
    "cpu_count": 8,
    "python_version": "3.13.1"
  },
  "runtime": {
    "uptime_seconds": 3600,
    "uptime_human": "1 hour, 0 minutes",
    "current_time": "2026-01-07T14:30:00.000Z",
    "timezone": "UTC"
  },
  "request": {
    "client_ip": "127.0.0.1",
    "user_agent": "curl/7.81.0",
    "method": "GET",
    "path": "/"
  },
  "endpoints": [
    {"path": "/", "method": "GET", "description": "Service information"},
    {"path": "/health", "method": "GET", "description": "Health check"}
  ]
}
```

**Response Fields:**

| Section | Field | Type | Description |
|---------|-------|------|-------------|
| `service` | `name` | string | Service identifier |
| | `version` | string | Service version |
| | `description` | string | Service purpose |
| | `framework` | string | Web framework used |
| `system` | `hostname` | string | System hostname |
| | `platform` | string | OS name (Linux/Darwin/Windows) |
| | `platform_version` | string | OS version/distribution |
| | `architecture` | string | System architecture |
| | `cpu_count` | integer | Number of CPU cores |
| | `python_version` | string | Python runtime version |
| `runtime` | `uptime_seconds` | integer | Service uptime in seconds |
| | `uptime_human` | string | Human-readable uptime |
| | `current_time` | string | Current UTC time (ISO format) |
| | `timezone` | string | Timezone of timestamps |
| `request` | `client_ip` | string | Client IP address |
| | `user_agent` | string | Client user agent string |
| | `method` | string | HTTP method used |
| | `path` | string | Requested path |
| `endpoints` | array | object | List of available endpoints |

### GET `/health` - Health Check

**Description:** Returns the health status of the service. Used for monitoring and load balancer health checks.

**HTTP Method:** GET

**Response Format:** JSON

**Example Request:**
```bash
curl http://localhost:5000/health
```

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T14:30:00.000Z",
  "uptime_seconds": 3600
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Service health status (always "healthy" when running) |
| `timestamp` | string | Current UTC time in ISO format |
| `uptime_seconds` | integer | Service uptime in seconds |

**HTTP Status Codes:**
- `200 OK`: Service is healthy and responding
- `5xx`: Service error (if unable to respond)

# Challenges & Solutions
None, I have a bunch of experience writing production grade backends on C++ and Java, so it was a piece of cake.

# GitHub Community

Starring repositories helps community to support the development and allows to bookmark repositories to return to them in the future. Also it helps stree to be seen by HRs and Developers of repositories and allows future career improvements.

Following others helps to improve one's networking, search for new job opportunities and learn from more experienced developers.
