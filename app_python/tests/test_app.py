import json
import time
from unittest.mock import patch
import pytest
from app import app, get_uptime_seconds, format_uptime_human


class TestMainEndpoint:
    """Test suite for the main endpoint (GET /)."""

    def test_service_info_structure(self, client):
        """Test that the main endpoint returns correct JSON structure."""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)

        # Test top-level keys
        assert 'service' in data
        assert 'system' in data
        assert 'runtime' in data
        assert 'request' in data
        assert 'endpoints' in data

        # Test service info
        service = data['service']
        assert service['name'] == 'devops-info-service'
        assert service['version'] == '1.0.0'
        assert service['framework'] == 'Flask'

        # Test system info presence
        system = data['system']
        assert 'hostname' in system
        assert 'platform' in system
        assert 'cpu_count' in system
        assert 'python_version' in system

        # Test runtime info
        runtime = data['runtime']
        assert 'uptime_seconds' in runtime
        assert 'uptime_human' in runtime
        assert 'current_time' in runtime
        assert 'timezone' in runtime
        assert runtime['timezone'] == 'UTC'

        # Test endpoints list
        endpoints = data['endpoints']
        assert len(endpoints) == 2
        assert endpoints[0]['path'] == '/'
        assert endpoints[1]['path'] == '/health'

    def test_service_info_with_mocked_system(self, client, mock_system_info):
        """Test system info with mocked data."""
        response = client.get('/')
        data = json.loads(response.data)

        system = data['system']
        assert system['hostname'] == 'test-host'
        assert system['platform'] == 'Linux'
        assert system['platform_version'] == 'Ubuntu 22.04'
        assert system['cpu_count'] == 4

    def test_request_info_in_response(self, client):
        """Test that request information is correctly captured."""
        headers = {'User-Agent': 'TestAgent/1.0'}
        response = client.get('/', headers=headers)
        data = json.loads(response.data)

        request_info = data['request']
        assert request_info['method'] == 'GET'
        assert request_info['path'] == '/'
        assert 'client_ip' in request_info

    def test_uptime_calculation(self, client):
        """Test that uptime is being calculated correctly."""
        response1 = client.get('/')
        data1 = json.loads(response1.data)
        uptime1 = data1['runtime']['uptime_seconds']

        time.sleep(1)

        response2 = client.get('/')
        data2 = json.loads(response2.data)
        uptime2 = data2['runtime']['uptime_seconds']

        assert uptime2 > uptime1
        assert uptime2 - uptime1 >= 1

    def test_uptime_human_formatting(self):
        """Test human-readable uptime formatting."""
        assert format_uptime_human(30) == "30 seconds"
        assert format_uptime_human(65) == "1 minute, 5 seconds"
        assert format_uptime_human(121) == "2 minutes, 1 second"
        assert format_uptime_human(3661) == "1 hour, 1 minute"
        assert format_uptime_human(7260) == "2 hours, 1 minute"
        assert format_uptime_human(90061) == "1 day, 1 hour"


class TestHealthEndpoint:
    """Test suite for the health check endpoint (GET /health)."""

    def test_health_check_structure(self, client):
        """Test that health endpoint returns correct JSON structure."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)

        assert 'status' in data
        assert 'timestamp' in data
        assert 'uptime_seconds' in data
        assert data['status'] == 'healthy'

    def test_health_check_iso_timestamp(self, client):
        """Test that timestamp is in ISO format."""
        response = client.get('/health')
        data = json.loads(response.data)

        timestamp = data['timestamp']
        # ISO format should end with 'Z' (UTC)
        assert timestamp.endswith('Z')
        # Should contain date and time separators
        assert 'T' in timestamp
        assert '-' in timestamp
        assert ':' in timestamp

    def test_health_check_consistency(self, client):
        """Test that multiple health checks return consistent data."""
        response1 = client.get('/health')
        response2 = client.get('/health')

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)

        assert data1['status'] == data2['status'] == 'healthy'
        assert data2['uptime_seconds'] >= data1['uptime_seconds']


class TestSystemInfo:
    """Test suite for system information collection."""

    @patch('app.platform.system')
    def test_system_info_linux(self, mock_system, client, monkeypatch):
        """Test system info collection on Linux platform."""
        mock_system.return_value = 'Linux'

        # Mock distro info
        mock_distro = pytest.importorskip('distro')
        monkeypatch.setattr('distro.name', lambda: 'Ubuntu')
        monkeypatch.setattr('distro.version', lambda: '22.04')

        response = client.get('/')
        data = json.loads(response.data)

        system = data['system']
        assert system['platform'] == 'Linux'
        assert 'Ubuntu' in system['platform_version']

    @patch('app.platform.system')
    def test_system_info_windows(self, mock_system):
        """Test system info collection on Windows platform."""
        mock_system.return_value = 'Windows'
        with patch('app.platform.win32_ver', return_value=('10', '', '', '')):
            from app import get_system_info
            info = get_system_info()
            assert info['platform'] == 'Windows'
            assert info['platform_version'] == '10'

    @patch('app.platform.system')
    def test_system_info_macos(self, mock_system):
        """Test system info collection on macOS platform."""
        mock_system.return_value = 'Darwin'
        with patch('app.platform.mac_ver', return_value=('12.6.0', ('', '', ''), '')):
            from app import get_system_info
            info = get_system_info()
            assert info['platform'] == 'Darwin'
            assert info['platform_version'] == '12.6.0'


class TestUptimeFunction:
    """Test suite for uptime calculation functions."""

    def test_get_uptime_seconds(self):
        """Test that uptime seconds returns an integer."""
        uptime = get_uptime_seconds()
        assert isinstance(uptime, int)
        assert uptime >= 0

    def test_uptime_monotonic(self):
        """Test that uptime only increases."""
        uptime1 = get_uptime_seconds()
        time.sleep(0.1)
        uptime2 = get_uptime_seconds()
        assert uptime2 >= uptime1


def test_json_content_type(client):
    """Test that responses have correct Content-Type header."""
    response = client.get('/')
    assert response.headers['Content-Type'] == 'application/json'

    response = client.get('/health')
    assert response.headers['Content-Type'] == 'application/json'