import json
import pytest


class TestErrorHandlers:
    """Test suite for error handlers."""

    def test_404_not_found(self, client):
        """Test 404 error handler."""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)

        assert 'error' in data
        assert 'message' in data
        assert data['error'] == 'Not Found'
        assert 'does not exist' in data['message']

    def test_405_method_not_allowed(self, client):
        """Test 405 error handler."""
        response = client.post('/')  # POST not allowed on main endpoint
        assert response.status_code == 405
        data = json.loads(response.data)

        assert 'error' in data
        assert 'message' in data
        assert data['error'] == 'Method Not Allowed'
        assert 'POST' in data['message']
        assert 'not allowed' in data['message']

    def test_405_on_health_endpoint(self, client):
        """Test 405 on health endpoint with wrong method."""
        response = client.put('/health')
        assert response.status_code == 405
        data = json.loads(response.data)

        assert data['error'] == 'Method Not Allowed'
        assert 'PUT' in data['message']

    @pytest.mark.parametrize("method", ['POST', 'PUT', 'DELETE', 'PATCH'])
    def test_multiple_invalid_methods(self, client, method):
        """Test that various HTTP methods return 405."""
        response = client.open('/', method=method)
        assert response.status_code == 405

    def test_error_response_structure(self, client):
        """Test that all error responses have consistent structure."""
        response = client.get('/invalid-path')
        data = json.loads(response.data)

        # All errors should have error and message fields
        assert set(data.keys()) == {'error', 'message'}
        assert isinstance(data['error'], str)
        assert isinstance(data['message'], str)