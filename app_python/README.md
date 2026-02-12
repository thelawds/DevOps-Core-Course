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

# Docker Image

## Obtaining the image

To build an image in-place - use `docker build -t app_python .`
To obtain the image from dockerhub - use `docker pull thelawds/app_python:latest`
To run the image - use `docker run -p 5000:5000 <Name>`, where `<Name>` is either `app_python` (or the tag you used to build the image) or `thelawds/app_python`(If you pulled the image from DockerHub) 

## Best Practices

I chose a base image with already preinstalled python - but slim version of it (without excess libraries) which is a good place to start even for production environment, but for a full-blown production environment I would search for an even lighter version of the image (possibly without any tools, just the interpreter and basic libs), which would work better with compiled languages (on multistage builds we can build an app with one image which includes compilers and needed tooling and run the app on a bare minimum linux version like Alpine), because now the image is a little heavy - 130MB.



## Build and Run process

### Building
```
alecsey@alecsey-B450-AORUS-ELITE:~/Documents/DevOps-Core-Course/app_python$ docker build -t thelawds/app_python:latest .
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Sending build context to Docker daemon  15.87kB
Step 1/7 : FROM python:3.13-slim
 ---> 7fda8cfe122c
Step 2/7 : WORKDIR /app
 ---> Using cache
 ---> cd684b6d6659
Step 3/7 : COPY requirements.txt .
 ---> Using cache
 ---> e450e4a1bcdf
Step 4/7 : COPY app.py .
 ---> 1dd83904ebe7
Step 5/7 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in 9b024996d82a
Collecting Flask==2.3.3 (from -r requirements.txt (line 1))
  Downloading flask-2.3.3-py3-none-any.whl.metadata (3.6 kB)
Collecting Werkzeug>=2.3.7 (from Flask==2.3.3->-r requirements.txt (line 1))
  Downloading werkzeug-3.1.5-py3-none-any.whl.metadata (4.0 kB)
Collecting Jinja2>=3.1.2 (from Flask==2.3.3->-r requirements.txt (line 1))
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting itsdangerous>=2.1.2 (from Flask==2.3.3->-r requirements.txt (line 1))
  Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting click>=8.1.3 (from Flask==2.3.3->-r requirements.txt (line 1))
  Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)
Collecting blinker>=1.6.2 (from Flask==2.3.3->-r requirements.txt (line 1))
  Downloading blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
Collecting MarkupSafe>=2.0 (from Jinja2>=3.1.2->Flask==2.3.3->-r requirements.txt (line 1))
  Downloading markupsafe-3.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Downloading flask-2.3.3-py3-none-any.whl (96 kB)
Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
Downloading click-8.3.1-py3-none-any.whl (108 kB)
Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
Downloading markupsafe-3.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
Downloading werkzeug-3.1.5-py3-none-any.whl (225 kB)
Installing collected packages: MarkupSafe, itsdangerous, click, blinker, Werkzeug, Jinja2, Flask

Successfully installed Flask-2.3.3 Jinja2-3.1.6 MarkupSafe-3.0.3 Werkzeug-3.1.5 blinker-1.9.0 click-8.3.1 itsdangerous-2.2.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.

[notice] A new release of pip is available: 25.3 -> 26.0
[notice] To update, run: pip install --upgrade pip
 ---> Removed intermediate container 9b024996d82a
 ---> ef0f097d31a8
Step 6/7 : EXPOSE 5000
 ---> Running in e6136dd9a4bb
 ---> Removed intermediate container e6136dd9a4bb
 ---> e5ef6c36ce38
Step 7/7 : CMD ["python", "app.py"]
 ---> Running in 62a5ee2a7784
 ---> Removed intermediate container 62a5ee2a7784
 ---> a26086b2efa4
Successfully built a26086b2efa4
Successfully tagged thelawds/app_python:latest
```

Dockerhub - `https://hub.docker.com/repository/docker/thelawds/app_python`

### Running:
**Curl Requests**:
```
alecsey@alecsey-B450-AORUS-ELITE:~/Documents/DevOps-Core-Course$ curl http://172.17.0.2:5000
{"endpoints":[{"description":"Service information","method":"GET","path":"/"},{"description":"Health check","method":"GET","path":"/health"}],"request":{"client_ip":"172.17.0.1","method":"GET","path":"/","user_agent":"Unknown"},"runtime":{"current_time":"2026-02-05T00:52:58.374Z","timezone":"UTC","uptime_human":"7 seconds","uptime_seconds":7},"service":{"description":"DevOps course info service","framework":"Flask","name":"devops-info-service","version":"1.0.0"},"system":{"architecture":"x86_64","cpu_count":16,"hostname":"1614dd52cfa2","platform":"Linux","platform_version":"#91~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 20 15:20:45 UTC 2","python_version":"3.13.12"}}

alecsey@alecsey-B450-AORUS-ELITE:~/Documents/DevOps-Core-Course$ curl http://172.17.0.2:5000
{"endpoints":[{"description":"Service information","method":"GET","path":"/"},{"description":"Health check","method":"GET","path":"/health"}],"request":{"client_ip":"172.17.0.1","method":"GET","path":"/","user_agent":"Unknown"},"runtime":{"current_time":"2026-02-05T00:53:01.262Z","timezone":"UTC","uptime_human":"9 seconds","uptime_seconds":9},"service":{"description":"DevOps course info service","framework":"Flask","name":"devops-info-service","version":"1.0.0"},"system":{"architecture":"x86_64","cpu_count":16,"hostname":"1614dd52cfa2","platform":"Linux","platform_version":"#91~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 20 15:20:45 UTC 2","python_version":"3.13.12"}}
```

**In docker**:
```
Calecsey@alecsey-B450-AORUS-ELITE:~/Documents/DevOps-Core-Course/app_python$ docker run -p 5000:5000 -p 80:80 app_python 
2026-02-05 00:52:51 - __main__ - INFO - Starting DevOps Info Service on 0.0.0.0:5000
2026-02-05 00:52:51 - __main__ - INFO - Debug mode: False
2026-02-05 00:52:51 - __main__ - INFO - Available endpoints: GET /, GET /health
 * Serving Flask app 'app'
 * Debug mode: off
2026-02-05 00:52:51 - werkzeug - INFO - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
2026-02-05 00:52:51 - werkzeug - INFO - Press CTRL+C to quit
/app/app.py:100: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  return datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
2026-02-05 00:52:58 - __main__ - INFO - Served main endpoint, uptime: 7s
2026-02-05 00:52:58 - werkzeug - INFO - 172.17.0.1 - - [05/Feb/2026 00:52:58] "GET / HTTP/1.1" 200 -
2026-02-05 00:53:01 - __main__ - INFO - Served main endpoint, uptime: 9s
2026-02-05 00:53:01 - werkzeug - INFO - 172.17.0.1 - - [05/Feb/2026 00:53:01] "GET / HTTP/1.1" 200 -
```


