import pytest

pytestmark = pytest.mark.django_db


def test_lista_states_retorna_200(api_client, states_3):
    resp = api_client.get('/api/states/')
    assert resp.status_code == 200


def test_lista_states_retorna_campos_corretos(api_client, states_3):
    resp = api_client.get('/api/states/')
    primeiro = resp.json()['results'][0]
    assert set(primeiro.keys()) == {'id', 'name', 'abbreviation'}


def test_lista_states_em_ordem_alfabetica(api_client, states_3):
    resp = api_client.get('/api/states/')
    nomes = [s['name'] for s in resp.json()['results']]
    assert nomes == sorted(nomes)


def test_lista_states_retorna_quantidade_correta(api_client, states_3):
    resp = api_client.get('/api/states/')
    assert resp.json()['count'] == 3


def test_returned_reflete_registros_da_pagina(api_client, states_3):
    resp = api_client.get('/api/states/')
    data = resp.json()
    assert data['returned'] == len(data['results'])


def test_busca_por_nome_retorna_resultado(api_client, states_3):
    resp = api_client.get('/api/states/?search=são')
    assert resp.json()['count'] == 1
    assert resp.json()['results'][0]['abbreviation'] == 'SP'


def test_busca_por_nome_parcial_retorna_resultado(api_client, states_3):
    resp = api_client.get('/api/states/?search=rio')
    assert resp.json()['count'] == 1
    assert resp.json()['results'][0]['abbreviation'] == 'RJ'


def test_busca_case_insensitive(api_client, states_3):
    resp_lower = api_client.get('/api/states/?search=minas')
    resp_upper = api_client.get('/api/states/?search=MINAS')
    assert resp_lower.json()['results'] == resp_upper.json()['results']


def test_busca_com_menos_de_3_caracteres_retorna_todos(api_client, states_3):
    resp = api_client.get('/api/states/?search=sã')
    assert resp.json()['count'] == 3


def test_busca_sem_resultado_retorna_lista_vazia(api_client, states_3):
    resp = api_client.get('/api/states/?search=xyz')
    assert resp.json()['results'] == []
