import pytest
from rest_framework.test import APIClient

from user.models import City, State


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def state(db):
    return State.objects.create(name='São Paulo', abbreviation='SP')


@pytest.fixture
def state_rj(db):
    return State.objects.create(name='Rio de Janeiro', abbreviation='RJ')


@pytest.fixture
def cities(state, state_rj):
    City.objects.create(name='Campinas', state=state)
    City.objects.create(name='São Paulo', state=state)
    City.objects.create(name='Rio de Janeiro', state=state_rj)


@pytest.fixture
def states_3(db):
    State.objects.create(name='São Paulo', abbreviation='SP')
    State.objects.create(name='Rio de Janeiro', abbreviation='RJ')
    State.objects.create(name='Minas Gerais', abbreviation='MG')


@pytest.fixture
def cities_10(state):
    for i in range(12):
        City.objects.create(name=f'Cidade {i:02d}', state=state)
