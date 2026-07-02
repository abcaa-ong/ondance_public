import pytest

from course.models import Course
from user.models import User

pytestmark = pytest.mark.django_db

MINE_URL = '/api/courses/mine/'


@pytest.fixture
def other_teacher(db):
    return User.objects.create_user(email='outro@teste.com', password='senha123')


@pytest.fixture
def other_course(other_teacher):
    return Course.objects.create(title='Forró', teacher=other_teacher, is_published=True)


# ── Autenticação ───────────────────────────────────────────────────────────


def test_anonimo_recebe_401(api_client):
    resp = api_client.get(MINE_URL)
    assert resp.status_code == 401


def test_autenticado_recebe_200(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(MINE_URL)
    assert resp.status_code == 200


# ── Filtragem por professor ────────────────────────────────────────────────


def test_retorna_apenas_cursos_do_professor_autenticado(
    api_client, teacher, published_course, other_course
):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(MINE_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert published_course.title in titulos
    assert other_course.title not in titulos


def test_nao_retorna_cursos_de_outro_professor(api_client, teacher, other_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(MINE_URL)
    assert resp.json()['results'] == []


def test_retorna_publicados_e_rascunhos(api_client, teacher, published_course, draft_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(MINE_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert published_course.title in titulos
    assert draft_course.title in titulos


# ── Estrutura da resposta ──────────────────────────────────────────────────


def test_retorna_campos_corretos(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(MINE_URL)
    curso = resp.json()['results'][0]
    assert set(curso.keys()) == {
        'id', 'title', 'description', 'duration', 'level', 'workload',
        'dance_style', 'emoji', 'thumb_bg', 'teacher', 'is_published', 'status',
        'modules_count', 'lessons_count',
    }


def test_teacher_no_response_e_email(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(MINE_URL)
    assert resp.json()['results'][0]['teacher'] == teacher.email


# ── Ordenação e lista vazia ────────────────────────────────────────────────


def test_lista_em_ordem_alfabetica(api_client, teacher):
    Course.objects.create(title='Zouk', teacher=teacher, is_published=True)
    Course.objects.create(title='Ballet', teacher=teacher, is_published=True)
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(MINE_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert titulos == sorted(titulos)


def test_lista_vazia_quando_professor_sem_cursos(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(MINE_URL)
    assert resp.json()['results'] == []
