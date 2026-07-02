import pytest

from course.models import Course
from user.models import Profile

pytestmark = pytest.mark.django_db

PUBLISHED_URL = '/api/courses/published/'


@pytest.fixture
def teacher_profile(teacher):
    return Profile.objects.create(user=teacher, name='Ana Lima')


# ── Acesso e status ────────────────────────────────────────────────────────


def test_retorna_200(api_client):
    resp = api_client.get(PUBLISHED_URL)
    assert resp.status_code == 200


def test_anonimo_pode_acessar(api_client, published_course, teacher_profile):
    resp = api_client.get(PUBLISHED_URL)
    assert resp.status_code == 200


def test_autenticado_pode_acessar(api_client, user, published_course, teacher_profile):
    api_client.force_authenticate(user=user)
    resp = api_client.get(PUBLISHED_URL)
    assert resp.status_code == 200


# ── Filtragem ──────────────────────────────────────────────────────────────


def test_retorna_apenas_cursos_publicados(api_client, published_course, draft_course, teacher_profile):
    resp = api_client.get(PUBLISHED_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert published_course.title in titulos
    assert draft_course.title not in titulos


def test_nao_retorna_cursos_em_rascunho(api_client, draft_course, teacher_profile):
    resp = api_client.get(PUBLISHED_URL)
    assert resp.json()['results'] == []


# ── Estrutura da resposta ──────────────────────────────────────────────────


def test_retorna_campos_do_curso(api_client, published_course, teacher_profile):
    resp = api_client.get(PUBLISHED_URL)
    curso = resp.json()['results'][0]
    assert set(curso.keys()) == {
        'id', 'title', 'description', 'duration', 'level', 'workload',
        'emoji', 'thumb_bg', 'teacher', 'is_published', 'status',
        'modules_count', 'lessons_count',
    }


def test_teacher_e_objeto_com_campos_corretos(api_client, published_course, teacher_profile):
    resp = api_client.get(PUBLISHED_URL)
    teacher_data = resp.json()['results'][0]['teacher']
    assert set(teacher_data.keys()) == {'id', 'email', 'name', 'photo'}


def test_teacher_name_retorna_nome_do_profile(api_client, published_course, teacher_profile):
    resp = api_client.get(PUBLISHED_URL)
    assert resp.json()['results'][0]['teacher']['name'] == 'Ana Lima'


def test_teacher_email_retorna_email_do_usuario(api_client, published_course, teacher, teacher_profile):
    resp = api_client.get(PUBLISHED_URL)
    assert resp.json()['results'][0]['teacher']['email'] == teacher.email


def test_teacher_sem_profile_retorna_nome_vazio(api_client, teacher):
    Course.objects.create(title='Samba', teacher=teacher, is_published=True)
    resp = api_client.get(PUBLISHED_URL)
    teacher_data = resp.json()['results'][0]['teacher']
    assert teacher_data['name'] == ''
    assert teacher_data['photo'] is None


# ── Ordenação ──────────────────────────────────────────────────────────────


def test_lista_em_ordem_alfabetica(api_client, teacher, teacher_profile):
    Course.objects.create(title='Zouk', teacher=teacher, is_published=True)
    Course.objects.create(title='Ballet', teacher=teacher, is_published=True)
    resp = api_client.get(PUBLISHED_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert titulos == sorted(titulos)
