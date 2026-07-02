import pytest

from course.models import Course, UserCourse
from user.models import Profile, User

pytestmark = pytest.mark.django_db

ENROLLMENTS_URL = '/api/enrollments/'


@pytest.fixture
def student(db):
    u = User.objects.create_user(email='aluno@teste.com', password='senha123')
    Profile.objects.create(user=u, name='João Aluno')
    return u


@pytest.fixture
def enrolled_course(teacher, student):
    course = Course.objects.create(
        title='Ballet Clássico',
        teacher=teacher,
        is_published=True,
        emoji='🩰',
        thumb_bg='#e91e63',
        level='Iniciante',
    )
    UserCourse.objects.create(profile=student.profile, course=course)
    return course


# ── Autenticação ───────────────────────────────────────────────────────────


def test_anonimo_recebe_401(api_client):
    resp = api_client.get(ENROLLMENTS_URL)
    assert resp.status_code == 401


# ── Listagem ───────────────────────────────────────────────────────────────


def test_aluno_ve_suas_matriculas(api_client, student, enrolled_course):
    api_client.force_authenticate(user=student)
    resp = api_client.get(ENROLLMENTS_URL)
    assert resp.status_code == 200
    results = resp.json()['results']
    assert len(results) == 1
    assert results[0]['course_title'] == 'Ballet Clássico'


def test_aluno_sem_matriculas_recebe_lista_vazia(api_client, student):
    api_client.force_authenticate(user=student)
    resp = api_client.get(ENROLLMENTS_URL)
    assert resp.json()['results'] == []


def test_nao_ve_matriculas_de_outro_aluno(api_client, student, enrolled_course, db):
    other = User.objects.create_user(email='outro@teste.com', password='senha123')
    Profile.objects.create(user=other)
    api_client.force_authenticate(user=other)
    resp = api_client.get(ENROLLMENTS_URL)
    assert resp.json()['results'] == []


# ── Campos do EnrollmentSerializer ─────────────────────────────────────────


def test_retorna_campos_do_curso(api_client, student, enrolled_course):
    api_client.force_authenticate(user=student)
    resp = api_client.get(ENROLLMENTS_URL)
    item = resp.json()['results'][0]
    assert set(item.keys()) == {
        'id', 'course', 'course_title', 'course_emoji', 'course_thumb_bg',
        'course_level', 'started_at', 'completed_at', 'is_completed',
        'progress_percent',
    }


def test_retorna_emoji_thumb_level_do_curso(api_client, student, enrolled_course):
    api_client.force_authenticate(user=student)
    resp = api_client.get(ENROLLMENTS_URL)
    item = resp.json()['results'][0]
    assert item['course_emoji'] == '🩰'
    assert item['course_thumb_bg'] == '#e91e63'
    assert item['course_level'] == 'Iniciante'


def test_is_completed_padrao_false(api_client, student, enrolled_course):
    api_client.force_authenticate(user=student)
    resp = api_client.get(ENROLLMENTS_URL)
    assert resp.json()['results'][0]['is_completed'] is False


def test_progress_percent_zero_sem_lessons(api_client, student, enrolled_course):
    api_client.force_authenticate(user=student)
    resp = api_client.get(ENROLLMENTS_URL)
    assert resp.json()['results'][0]['progress_percent'] == 0


# ── Ordenação ──────────────────────────────────────────────────────────────


def test_ordem_por_started_at_desc(api_client, student, teacher):
    c1 = Course.objects.create(title='Zouk', teacher=teacher, is_published=True)
    c2 = Course.objects.create(title='Samba', teacher=teacher, is_published=True)
    UserCourse.objects.create(profile=student.profile, course=c1)
    UserCourse.objects.create(profile=student.profile, course=c2)
    api_client.force_authenticate(user=student)
    resp = api_client.get(ENROLLMENTS_URL)
    titles = [r['course_title'] for r in resp.json()['results']]
    assert titles == ['Samba', 'Zouk']
