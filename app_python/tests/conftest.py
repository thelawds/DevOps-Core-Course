import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_system_info(monkeypatch):
    """Mock system info for consistent test results."""
    def mock_get_system_info():
        return {
            "hostname": "test-host",
            "platform": "Linux",
            "platform_version": "Ubuntu 22.04",
            "architecture": "x86_64",
            "cpu_count": 4,
            "python_version": "3.13.0"
        }
    monkeypatch.setattr('app.get_system_info', mock_get_system_info)