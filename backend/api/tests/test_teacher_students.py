import pytest

from course.models import UserCourse
from user.models import Profile, User

pytestmark = pytest.mark.django_db

STUDENTS_URL = '/api/teacher/students/'


@pytest.fixture
def other_teacher(db):
    return User.objects.create_user(email='outro@teste.com', password='senha123')


@pytest.fixture
def student_user(db):
    u = User.objects.create_user(email='aluno@teste.com', password='senha123')
    Profile.objects.create(user=u, name='João Aluno')
    return u


@pytest.fixture
def student_profile(student_user):
    return student_user.profile


@pytest.fixture
def enrollment(student_profile, published_course):
    return UserCourse.objects.create(profile=student_profile, course=published_course)


@pytest.fixture
def other_course(other_teacher):
    from course.models import Course
    return Course.objects.create(title='Samba', teacher=other_teacher)


@pytest.fixture
def other_enrollment(student_profile, other_course):
    return UserCourse.objects.create(profile=student_profile, course=other_course)


# ── Autenticação ───────────────────────────────────────────────────────────


def test_anonimo_recebe_401(api_client):
    resp = api_client.get(STUDENTS_URL)
    assert resp.status_code == 401


def test_autenticado_recebe_200(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    assert resp.status_code == 200


# ── Estrutura da resposta ──────────────────────────────────────────────────


def test_retorna_campos_corretos(api_client, teacher, enrollment):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    item = resp.json()['results'][0]
    assert set(item.keys()) == {
        'id', 'student_name', 'student_email', 'student_photo',
        'course_id', 'course_title', 'started_at', 'is_completed',
    }


def test_retorna_nome_e_email_do_aluno(api_client, teacher, enrollment, student_user):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    item = resp.json()['results'][0]
    assert item['student_name'] == 'João Aluno'
    assert item['student_email'] == student_user.email


def test_retorna_titulo_do_curso(api_client, teacher, enrollment, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    assert resp.json()['results'][0]['course_title'] == published_course.title


def test_student_photo_e_none_sem_foto(api_client, teacher, enrollment):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    assert resp.json()['results'][0]['student_photo'] is None


def test_is_completed_padrao_e_false(api_client, teacher, enrollment):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    assert resp.json()['results'][0]['is_completed'] is False


def test_is_completed_true_quando_concluido(api_client, teacher, enrollment):
    enrollment.is_completed = True
    enrollment.save()
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    assert resp.json()['results'][0]['is_completed'] is True


# ── Isolamento por professor ───────────────────────────────────────────────


def test_retorna_apenas_alunos_dos_proprios_cursos(api_client, teacher, enrollment, other_enrollment):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    course_titles = [e['course_title'] for e in resp.json()['results']]
    assert all(t == enrollment.course.title for t in course_titles)


def test_nao_retorna_alunos_de_outros_professores(api_client, teacher, other_enrollment):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    assert resp.json()['results'] == []


def test_lista_vazia_sem_matriculas(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    assert resp.json()['results'] == []


# ── Filtro por course_id ───────────────────────────────────────────────────


def test_filtra_por_course_id(api_client, teacher, enrollment, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL, {'course_id': str(published_course.id)})
    assert len(resp.json()['results']) == 1
    assert resp.json()['results'][0]['course_title'] == published_course.title


def test_filtro_course_id_inexistente_retorna_vazio(api_client, teacher, enrollment):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL, {'course_id': '00000000-0000-0000-0000-000000000000'})
    assert resp.json()['results'] == []


def test_filtro_course_id_de_outro_professor_retorna_vazio(api_client, teacher, other_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL, {'course_id': str(other_course.id)})
    assert resp.json()['results'] == []


# ── Múltiplos alunos e cursos ──────────────────────────────────────────────


def test_retorna_multiplas_matriculas(api_client, teacher, published_course, draft_course):
    for i in range(3):
        u = User.objects.create_user(email=f'aluno{i}@teste.com', password='senha123')
        p = Profile.objects.create(user=u, name=f'Aluno {i}')
        UserCourse.objects.create(profile=p, course=published_course)
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(STUDENTS_URL)
    assert resp.json()['count'] == 3
