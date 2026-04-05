import pytest

from user.models import City, Profile, State, User

pytestmark = pytest.mark.django_db


def test_create_user_with_profile_minimal(api_client):
    payload = {
        'email': 'aluno@teste.com',
        'password': 'senha1234',
        'name': 'Aluno Teste',
    }
    resp = api_client.post('/api/users/', data=payload, format='json')

    assert resp.status_code == 201
    user = User.objects.get(email='aluno@teste.com')
    assert user.check_password('senha1234') is True
    assert Profile.objects.filter(user=user, name='Aluno Teste').exists() is True

    profile = Profile.objects.get(user=user)
    assert profile.city is None
    assert profile.celular is None


def test_create_user_with_profile_city_celular(api_client, state):
    city = City.objects.create(name='Campinas', state=state)
    payload = {
        'email': 'aluna@teste.com',
        'password': 'senha1234',
        'name': 'Aluna Teste',
        'city': str(city.id),
        'celular': '11999999999',
    }
    resp = api_client.post('/api/users/', data=payload, format='json')

    assert resp.status_code == 201
    user = User.objects.get(email='aluna@teste.com')
    profile = Profile.objects.get(user=user)
    assert profile.city == city
    assert profile.celular == '11999999999'


def test_create_user_rejects_duplicate_email_case_insensitive(api_client):
    User.objects.create_user(email='dup@teste.com', password='senha1234')
    payload = {
        'email': 'DUP@TESTE.COM',
        'password': 'senha1234',
        'name': 'Aluno',
    }
    resp = api_client.post('/api/users/', data=payload, format='json')

    assert resp.status_code == 400
    assert 'email' in resp.data


def test_create_user_rejects_short_password(api_client):
    payload = {
        'email': 'curta@teste.com',
        'password': '1234567',
        'name': 'Aluno',
    }
    resp = api_client.post('/api/users/', data=payload, format='json')

    assert resp.status_code == 400
    assert 'password' in resp.data


def test_create_user_requires_name(api_client):
    payload = {
        'email': 'semnome@teste.com',
        'password': 'senha1234',
    }
    resp = api_client.post('/api/users/', data=payload, format='json')

    assert resp.status_code == 400
    assert 'name' in resp.data
