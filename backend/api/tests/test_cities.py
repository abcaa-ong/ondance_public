import pytest

pytestmark = pytest.mark.django_db


def test_lista_cidades_retorna_200(api_client, cities):
    resp = api_client.get('/api/cities/')
    assert resp.status_code == 200


def test_returned_reflete_registros_da_pagina(api_client, cities):
    resp = api_client.get('/api/cities/')
    data = resp.json()
    assert data['returned'] == len(data['results'])


def test_page_size_padrao_e_10(api_client, cities_10):
    resp = api_client.get('/api/cities/')
    assert resp.json()['returned'] == 10


def test_lista_cidades_retorna_campos_corretos(api_client, cities):
    resp = api_client.get('/api/cities/')
    primeira = resp.json()['results'][0]
    assert set(primeira.keys()) == {'id', 'name', 'state'}


def test_lista_cidades_em_ordem_alfabetica(api_client, cities):
    resp = api_client.get('/api/cities/')
    nomes = [c['name'] for c in resp.json()['results']]
    assert nomes == sorted(nomes)


def test_filtra_cidades_por_estado(api_client, cities):
    resp = api_client.get('/api/cities/?state=SP')
    results = resp.json()['results']
    assert len(results) == 2
    assert all(c['state'] == 'SP' for c in results)


def test_filtra_estado_inexistente_retorna_lista_vazia(api_client, cities):
    resp = api_client.get('/api/cities/?state=XX')
    assert resp.json()['results'] == []


def test_filtra_estado_case_insensitive(api_client, cities):
    resp_upper = api_client.get('/api/cities/?state=SP')
    resp_lower = api_client.get('/api/cities/?state=sp')
    assert resp_upper.json()['results'] == resp_lower.json()['results']


def test_state_no_response_e_sigla(api_client, cities):
    resp = api_client.get('/api/cities/?state=RJ')
    assert resp.json()['results'][0]['state'] == 'RJ'
