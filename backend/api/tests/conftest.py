import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from course.models import Course
from user.models import City, Profile, State, User


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


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


@pytest.fixture
def user(db):
    u = User.objects.create_user(email='usuario@teste.com', password='senha123')
    Profile.objects.create(user=u)
    return u


@pytest.fixture
def city(state):
    return City.objects.create(name='Campinas', state=state)


@pytest.fixture
def admin_user(db):
    u = User.objects.create_user(email='admin@teste.com', password='senha123', is_staff=True)
    Profile.objects.create(user=u, name='Admin')
    return u


@pytest.fixture
def teacher(db):
    return User.objects.create_user(email='teacher@teste.com', password='senha123')


@pytest.fixture
def published_course(teacher):
    return Course.objects.create(title='Ballet Clássico', teacher=teacher, is_published=True)


@pytest.fixture
def draft_course(teacher):
    return Course.objects.create(title='Jazz Avançado', teacher=teacher, is_published=False)
