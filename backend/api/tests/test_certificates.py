import pytest

from course.models import Certificate, Course, UserCourse
from user.models import Profile, User

pytestmark = pytest.mark.django_db

CERT_URL = '/api/certificates/'


@pytest.fixture
def student(db):
    u = User.objects.create_user(email='aluno@teste.com', password='senha123')
    Profile.objects.create(user=u, name='João Aluno')
    return u


@pytest.fixture
def completed_enrollment(student, teacher):
    course = Course.objects.create(
        title='Ballet Clássico',
        teacher=teacher,
        is_published=True,
        emoji='🩰',
        thumb_bg='#e91e63',
        level='Iniciante',
        workload=40,
    )
    return UserCourse.objects.create(
        profile=student.profile,
        course=course,
        is_completed=True,
        completed_at='2025-01-15T10:00:00Z',
    )


@pytest.fixture
def certificate(completed_enrollment):
    return Certificate.objects.create(
        profile=completed_enrollment.profile,
        course=completed_enrollment.course,
        code='ABC-2025-001',
    )


# ── Autenticação ───────────────────────────────────────────────────────────


def test_anonimo_recebe_401(api_client):
    resp = api_client.get(CERT_URL)
    assert resp.status_code == 401


# ── Listagem ───────────────────────────────────────────────────────────────


def test_aluno_ve_seus_certificados(api_client, student, certificate):
    api_client.force_authenticate(user=student)
    resp = api_client.get(CERT_URL)
    assert resp.status_code == 200
    results = resp.json()['results']
    assert len(results) == 1
    assert results[0]['code'] == 'ABC-2025-001'


def test_aluno_sem_certificados_recebe_lista_vazia(api_client, student):
    api_client.force_authenticate(user=student)
    resp = api_client.get(CERT_URL)
    assert resp.json()['results'] == []


def test_nao_ve_certificados_de_outro_aluno(api_client, student, certificate, db):
    other = User.objects.create_user(email='outro@teste.com', password='senha123')
    Profile.objects.create(user=other)
    api_client.force_authenticate(user=other)
    resp = api_client.get(CERT_URL)
    assert resp.json()['results'] == []


# ── Campos do CertificateSerializer ────────────────────────────────────────


def test_retorna_campos_corretos(api_client, student, certificate):
    api_client.force_authenticate(user=student)
    resp = api_client.get(CERT_URL)
    item = resp.json()['results'][0]
    assert set(item.keys()) == {
        'id', 'code', 'course', 'course_title', 'course_emoji',
        'course_thumb_bg', 'course_level', 'course_workload',
        'teacher_name', 'issue_date', 'file',
    }


def test_retorna_dados_do_curso(api_client, student, certificate):
    api_client.force_authenticate(user=student)
    resp = api_client.get(CERT_URL)
    item = resp.json()['results'][0]
    assert item['course_title'] == 'Ballet Clássico'
    assert item['course_emoji'] == '🩰'
    assert item['course_thumb_bg'] == '#e91e63'
    assert item['course_level'] == 'Iniciante'
    assert item['course_workload'] == 40


def test_retorna_nome_do_professor(api_client, student, certificate, teacher):
    api_client.force_authenticate(user=student)
    resp = api_client.get(CERT_URL)
    item = resp.json()['results'][0]
    assert item['teacher_name'] == teacher.email


# ── Ordenação ──────────────────────────────────────────────────────────────


def test_ordem_por_issue_date_desc(api_client, student, teacher):
    import datetime
    c1 = Course.objects.create(title='Zouk', teacher=teacher, is_published=True)
    c2 = Course.objects.create(title='Samba', teacher=teacher, is_published=True)
    cert1 = Certificate.objects.create(profile=student.profile, course=c1, code='C-001')
    cert2 = Certificate.objects.create(profile=student.profile, course=c2, code='C-002')
    Certificate.objects.filter(id=cert1.id).update(issue_date=datetime.date(2025, 1, 10))
    Certificate.objects.filter(id=cert2.id).update(issue_date=datetime.date(2025, 6, 1))
    api_client.force_authenticate(user=student)
    resp = api_client.get(CERT_URL)
    codes = [r['code'] for r in resp.json()['results']]
    assert codes == ['C-002', 'C-001']
