# DevOps Info Service Documentation

## Overview

The DevOps Info Service is a lightweight Flask-based web service that provides comprehensive system and service information. It's designed for monitoring, debugging, and demonstrating DevOps principles in action. The service exposes two main endpoints that return detailed JSON responses about the service itself, the underlying system, and runtime metrics.

## Prerequisites

- Python 3.8 or higher
- Flask 2.3.3

## API Endpoints

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

## Configuration

The service can be configured using environment variables. All configuration options have sensible defaults.

### Environment Variables Reference

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `HOST` | `0.0.0.0` | Network interface to bind to | `127.0.0.1` (localhost only) |
| `PORT` | `5000` | Port number to listen on | `8080`, `3000` |
| `DEBUG` | `False` | Enable Flask debug mode | `true`, `false` |

```bash
export HOST=127.0.0.1
export PORT=5000
export DEBUG=true
python app.py
```
