import pytest

from user.models import Profile, User

pytestmark = pytest.mark.django_db

PROFILE_URL = '/api/profile/'
PROFILES_URL = '/api/profiles/'


# ── GET ────────────────────────────────────────────────────────────────────


def test_get_requer_autenticacao(api_client):
    resp = api_client.get(PROFILE_URL)
    assert resp.status_code == 401


def test_get_retorna_200_para_usuario_autenticado(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.get(PROFILE_URL)
    assert resp.status_code == 200


def test_get_retorna_campos_corretos(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.get(PROFILE_URL)
    campos_esperados = {'email', 'name', 'photo', 'celular', 'telephone', 'birthday', 'city', 'city_detail'}
    assert campos_esperados.issubset(resp.data.keys())


def test_get_retorna_email_do_usuario(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.get(PROFILE_URL)
    assert resp.data['email'] == user.email


def test_get_retorna_nome_do_profile(api_client, user):
    user.profile.name = 'Ana Lima'
    user.profile.save()
    api_client.force_authenticate(user=user)
    resp = api_client.get(PROFILE_URL)
    assert resp.data['name'] == 'Ana Lima'


def test_get_city_detail_e_none_sem_cidade(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.get(PROFILE_URL)
    assert resp.data['city_detail'] is None


def test_get_city_detail_contem_nome_e_estado(api_client, user, city):
    user.profile.city = city
    user.profile.save()
    api_client.force_authenticate(user=user)
    resp = api_client.get(PROFILE_URL)
    assert resp.data['city_detail']['name'] == city.name
    assert resp.data['city_detail']['state'] == city.state.abbreviation


# ── PATCH ──────────────────────────────────────────────────────────────────


def test_patch_requer_autenticacao(api_client):
    resp = api_client.patch(PROFILE_URL, {'name': 'Novo Nome'}, format='json')
    assert resp.status_code == 401


def test_patch_atualiza_nome(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(PROFILE_URL, {'name': 'Maria Silva'}, format='json')
    assert resp.status_code == 200
    assert resp.data['name'] == 'Maria Silva'


def test_patch_persiste_nome_no_banco(api_client, user):
    api_client.force_authenticate(user=user)
    api_client.patch(PROFILE_URL, {'name': 'Carlos Moura'}, format='json')
    user.profile.refresh_from_db()
    assert user.profile.name == 'Carlos Moura'


def test_patch_atualiza_celular(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(PROFILE_URL, {'celular': '11999999999'}, format='json')
    assert resp.status_code == 200
    assert resp.data['celular'] == '11999999999'


def test_patch_atualiza_telephone(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(PROFILE_URL, {'telephone': '1133334444'}, format='json')
    assert resp.status_code == 200
    assert resp.data['telephone'] == '1133334444'


def test_patch_atualiza_birthday(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(PROFILE_URL, {'birthday': '1995-06-15'}, format='json')
    assert resp.status_code == 200
    assert resp.data['birthday'] == '1995-06-15'


def test_patch_atualiza_city(api_client, user, city):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(PROFILE_URL, {'city': str(city.id)}, format='json')
    assert resp.status_code == 200
    assert resp.data['city_detail']['name'] == city.name


def test_patch_com_celular_retorna_profile_complete_true(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(PROFILE_URL, {'celular': '11988888888'}, format='json')
    assert resp.data['profile_complete'] is True


def test_patch_sem_celular_retorna_profile_complete_false(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(PROFILE_URL, {'name': 'Sem Celular'}, format='json')
    assert resp.data['profile_complete'] is False


def test_patch_e_parcial_preserva_campos_anteriores(api_client, user):
    api_client.force_authenticate(user=user)
    api_client.patch(PROFILE_URL, {'name': 'João'}, format='json')
    resp = api_client.patch(PROFILE_URL, {'celular': '11988887777'}, format='json')
    assert resp.data['name'] == 'João'
    assert resp.data['celular'] == '11988887777'


def test_patch_permite_limpar_celular(api_client, user):
    api_client.force_authenticate(user=user)
    api_client.patch(PROFILE_URL, {'celular': '11999999999'}, format='json')
    resp = api_client.patch(PROFILE_URL, {'celular': None}, format='json')
    assert resp.status_code == 200
    assert resp.data['celular'] is None


# ── GET /api/profiles/ ─────────────────────────────────────────────────────


def test_profiles_anonimo_recebe_401(api_client):
    resp = api_client.get(PROFILES_URL)
    assert resp.status_code == 401


def test_profiles_usuario_comum_recebe_403(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.get(PROFILES_URL)
    assert resp.status_code == 403


def test_profiles_admin_recebe_200(api_client, admin_user):
    resp = api_client.get(PROFILES_URL)
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(PROFILES_URL)
    assert resp.status_code == 200


def test_profiles_retorna_campos_paginados(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(PROFILES_URL)
    assert {'count', 'returned', 'next', 'previous', 'results'}.issubset(resp.data.keys())


def test_profiles_paginacao_limita_10_por_pagina(api_client, admin_user):
    for i in range(15):
        u = User.objects.create_user(email=f'extra{i}@teste.com', password='senha123')
        Profile.objects.create(user=u, name=f'Extra {i}')
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(PROFILES_URL)
    assert resp.data['returned'] <= 10
    assert resp.data['count'] >= 15
