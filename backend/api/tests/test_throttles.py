import pytest
from unittest.mock import patch

pytestmark = pytest.mark.django_db


def test_register_throttle_returns_429_when_limit_exceeded(api_client):
    with patch('api.throttles.RegisterThrottle.allow_request', return_value=False), \
         patch('api.throttles.RegisterThrottle.wait', return_value=60.0):
        resp = api_client.post(
            '/api/register/',
            data={'email': 'x@teste.com', 'password': 'senha1234'},
            format='json',
        )

    assert resp.status_code == 429
