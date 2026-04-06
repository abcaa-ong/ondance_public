import pytest

from user.models import Profile, User

pytestmark = pytest.mark.django_db


def test_create_user(api_client):
    payload = {'email': 'aluno@teste.com', 'password': 'senha1234'}
    resp = api_client.post('/api/register/', data=payload, format='json')

    assert resp.status_code == 201
    user = User.objects.get(email='aluno@teste.com')
    assert user.check_password('senha1234') is True
    assert Profile.objects.filter(user=user).exists() is True


def test_create_user_rejects_duplicate_email_case_insensitive(api_client):
    User.objects.create_user(email='dup@teste.com', password='senha1234')
    payload = {'email': 'DUP@TESTE.COM', 'password': 'senha1234'}
    resp = api_client.post('/api/register/', data=payload, format='json')

    assert resp.status_code == 400
    assert 'email' in resp.data


def test_create_user_rejects_short_password(api_client):
    payload = {'email': 'curta@teste.com', 'password': '1234567'}
    resp = api_client.post('/api/register/', data=payload, format='json')

    assert resp.status_code == 400
    assert 'password' in resp.data
