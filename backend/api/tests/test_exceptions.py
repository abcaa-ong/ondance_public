import pytest

pytestmark = pytest.mark.django_db


def test_register_duplicate_email_returns_message(api_client):
    payload = {'email': 'dup@teste.com', 'password': 'senha1234'}
    api_client.post('/api/register/', data=payload, format='json')

    resp = api_client.post('/api/register/', data=payload, format='json')

    assert resp.status_code == 400
    assert resp.data['message'] == 'E-mail já cadastrado.'


def test_register_short_password_returns_message(api_client):
    payload = {'email': 'curta@teste.com', 'password': '123'}
    resp = api_client.post('/api/register/', data=payload, format='json')

    assert resp.status_code == 400
    assert 'message' in resp.data
    assert '8' in resp.data['message']


def test_login_wrong_credentials_returns_message(api_client):
    resp = api_client.post('/api/token/', data={'email': 'x@x.com', 'password': 'errada123'}, format='json')

    assert resp.status_code == 401
    assert resp.data['message'] == 'E-mail ou senha inválidos.'
