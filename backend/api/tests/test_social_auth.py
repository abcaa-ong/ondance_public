import pytest
from unittest.mock import MagicMock, patch

from allauth.socialaccount.models import SocialAccount
from user.models import Profile, User

pytestmark = pytest.mark.django_db

URL = '/api/auth/social/google/'
CLIENT_ID = 'test-client-id.apps.googleusercontent.com'

VALID_PAYLOAD = {
    'sub': 'google-uid-123',
    'email': 'joao@gmail.com',
    'email_verified': 'true',
    'name': 'João Silva',
    'aud': CLIENT_ID,
}


def _mock_google(payload=None, status_code=200, raise_exc=None):
    """Helper para mockar requests.get no serializer."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = payload or VALID_PAYLOAD
    if raise_exc:
        return patch('api.serializers.http_requests.get', side_effect=raise_exc)
    return patch('api.serializers.http_requests.get', return_value=mock_resp)


# --- Cenário feliz ---

def test_google_auth_novo_usuario_cria_user_profile_social_account(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID

    with _mock_google():
        resp = api_client.post(URL, {'credential': 'fake-token'}, format='json')

    assert resp.status_code == 200
    assert 'access' in resp.data
    assert 'refresh' in resp.data
    assert User.objects.filter(email='joao@gmail.com').exists()
    assert Profile.objects.filter(user__email='joao@gmail.com').exists()
    assert SocialAccount.objects.filter(provider='google', uid='google-uid-123').exists()


def test_google_auth_profile_criado_com_nome_do_google(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID

    with _mock_google():
        api_client.post(URL, {'credential': 'fake-token'}, format='json')

    profile = Profile.objects.get(user__email='joao@gmail.com')
    assert profile.name == 'João Silva'


def test_google_auth_fallback_nome_para_parte_local_do_email(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID
    payload = {**VALID_PAYLOAD, 'name': ''}

    with _mock_google(payload=payload):
        api_client.post(URL, {'credential': 'fake-token'}, format='json')

    profile = Profile.objects.get(user__email='joao@gmail.com')
    assert profile.name == 'joao'


def test_google_auth_usuario_existente_via_social_account_nao_duplica(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID
    user = User.objects.create_user(email='joao@gmail.com', password='senha1234')
    Profile.objects.create(user=user, name='João Antigo')
    SocialAccount.objects.create(provider='google', uid='google-uid-123', user=user)

    with _mock_google():
        resp = api_client.post(URL, {'credential': 'fake-token'}, format='json')

    assert resp.status_code == 200
    assert User.objects.filter(email='joao@gmail.com').count() == 1


def test_google_auth_usuario_com_email_ja_existente_vincula_social_account(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID
    user = User.objects.create_user(email='joao@gmail.com', password='senha1234')
    Profile.objects.create(user=user, name='João')

    with _mock_google():
        resp = api_client.post(URL, {'credential': 'fake-token'}, format='json')

    assert resp.status_code == 200
    assert User.objects.filter(email='joao@gmail.com').count() == 1
    assert SocialAccount.objects.filter(provider='google', uid='google-uid-123', user=user).exists()


def test_google_auth_novo_usuario_tem_senha_inutilizavel(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID

    with _mock_google():
        api_client.post(URL, {'credential': 'fake-token'}, format='json')

    user = User.objects.get(email='joao@gmail.com')
    assert not user.has_usable_password()


# --- Erros de validação ---

def test_google_auth_token_invalido_retorna_400(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID

    with _mock_google(status_code=400, payload={'error': 'invalid_token'}):
        resp = api_client.post(URL, {'credential': 'token-invalido'}, format='json')

    assert resp.status_code == 400
    assert resp.data['message'] == 'Token do Google inválido ou expirado.'


def test_google_auth_aud_errado_retorna_400(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID
    payload = {**VALID_PAYLOAD, 'aud': 'outro-client-id'}

    with _mock_google(payload=payload):
        resp = api_client.post(URL, {'credential': 'fake-token'}, format='json')

    assert resp.status_code == 400
    assert resp.data['message'] == 'Token não autorizado para esta aplicação.'


def test_google_auth_email_nao_verificado_retorna_400(api_client, settings):
    settings.GOOGLE_CLIENT_ID = CLIENT_ID
    payload = {**VALID_PAYLOAD, 'email_verified': 'false'}

    with _mock_google(payload=payload):
        resp = api_client.post(URL, {'credential': 'fake-token'}, format='json')

    assert resp.status_code == 400
    assert resp.data['message'] == 'E-mail da conta Google não verificado.'


def test_google_auth_erro_de_rede_retorna_400(api_client, settings):
    import requests
    settings.GOOGLE_CLIENT_ID = CLIENT_ID

    with _mock_google(raise_exc=requests.RequestException('timeout')):
        resp = api_client.post(URL, {'credential': 'fake-token'}, format='json')

    assert resp.status_code == 400
    assert resp.data['message'] == 'Não foi possível verificar o token com o Google.'


def test_google_auth_sem_credential_retorna_400(api_client):
    resp = api_client.post(URL, {}, format='json')

    assert resp.status_code == 400
    assert 'message' in resp.data


# --- Throttle ---

def test_google_auth_throttle_retorna_429(api_client):
    with patch('api.throttles.SocialAuthThrottle.allow_request', return_value=False), \
         patch('api.throttles.SocialAuthThrottle.wait', return_value=60.0):
        resp = api_client.post(URL, {'credential': 'fake'}, format='json')

    assert resp.status_code == 429
