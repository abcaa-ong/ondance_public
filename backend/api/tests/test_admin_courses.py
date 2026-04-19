import pytest

from course.models import Course
from user.models import Profile

pytestmark = pytest.mark.django_db

ADMIN_URL = '/api/admin/courses/'


@pytest.fixture
def teacher_profile(teacher):
    return Profile.objects.create(user=teacher, name='Ana Lima')


@pytest.fixture
def pending_course(teacher):
    return Course.objects.create(title='Ballet Clássico', teacher=teacher, status='PENDING', is_published=False)


@pytest.fixture
def approved_course(teacher):
    return Course.objects.create(title='Jazz Avançado', teacher=teacher, status='APPROVED', is_published=True)


@pytest.fixture
def rejected_course(teacher):
    return Course.objects.create(title='Samba Raiz', teacher=teacher, status='REJECTED', is_published=False)


# ── Autenticação e permissão ───────────────────────────────────────────────


def test_anonimo_recebe_401(api_client):
    resp = api_client.get(ADMIN_URL)
    assert resp.status_code == 401


def test_usuario_comum_recebe_403(api_client, user):
    api_client.force_authenticate(user=user)
    resp = api_client.get(ADMIN_URL)
    assert resp.status_code == 403


def test_professor_recebe_403(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(ADMIN_URL)
    assert resp.status_code == 403


def test_admin_recebe_200(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL)
    assert resp.status_code == 200


# ── Listagem ───────────────────────────────────────────────────────────────


def test_lista_todos_os_cursos(api_client, admin_user, pending_course, approved_course, rejected_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert pending_course.title in titulos
    assert approved_course.title in titulos
    assert rejected_course.title in titulos


def test_retorna_campos_corretos(api_client, admin_user, pending_course, teacher_profile):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL)
    curso = resp.json()['results'][0]
    assert set(curso.keys()) == {'id', 'title', 'teacher', 'status', 'is_published'}


def test_teacher_e_objeto_aninhado(api_client, admin_user, pending_course, teacher_profile):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL)
    teacher_data = resp.json()['results'][0]['teacher']
    assert set(teacher_data.keys()) == {'id', 'email', 'name', 'photo'}
    assert teacher_data['name'] == 'Ana Lima'


def test_lista_em_ordem_alfabetica(api_client, admin_user, teacher):
    Course.objects.create(title='Zouk', teacher=teacher)
    Course.objects.create(title='Ballet', teacher=teacher)
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert titulos == sorted(titulos)


# ── Filtro por status ──────────────────────────────────────────────────────


def test_filtra_por_status_pending(api_client, admin_user, pending_course, approved_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL, {'status': 'PENDING'})
    titulos = [c['title'] for c in resp.json()['results']]
    assert pending_course.title in titulos
    assert approved_course.title not in titulos


def test_filtra_por_status_approved(api_client, admin_user, pending_course, approved_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL, {'status': 'APPROVED'})
    titulos = [c['title'] for c in resp.json()['results']]
    assert approved_course.title in titulos
    assert pending_course.title not in titulos


def test_filtra_por_status_rejected(api_client, admin_user, rejected_course, pending_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL, {'status': 'REJECTED'})
    titulos = [c['title'] for c in resp.json()['results']]
    assert rejected_course.title in titulos
    assert pending_course.title not in titulos


def test_filtra_status_case_insensitive(api_client, admin_user, pending_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL, {'status': 'pending'})
    titulos = [c['title'] for c in resp.json()['results']]
    assert pending_course.title in titulos


def test_sem_filtro_retorna_todos(api_client, admin_user, pending_course, approved_course, rejected_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.get(ADMIN_URL)
    assert resp.json()['count'] == 3


# ── Aprovar ────────────────────────────────────────────────────────────────


def test_anonimo_nao_pode_aprovar(api_client, pending_course):
    resp = api_client.post(f'{ADMIN_URL}{pending_course.id}/approve/')
    assert resp.status_code == 401


def test_usuario_comum_nao_pode_aprovar(api_client, user, pending_course):
    api_client.force_authenticate(user=user)
    resp = api_client.post(f'{ADMIN_URL}{pending_course.id}/approve/')
    assert resp.status_code == 403


def test_admin_aprova_curso(api_client, admin_user, pending_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.post(f'{ADMIN_URL}{pending_course.id}/approve/')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'APPROVED'
    assert resp.json()['is_published'] is True


def test_aprovar_persiste_no_banco(api_client, admin_user, pending_course):
    api_client.force_authenticate(user=admin_user)
    api_client.post(f'{ADMIN_URL}{pending_course.id}/approve/')
    pending_course.refresh_from_db()
    assert pending_course.status == 'APPROVED'
    assert pending_course.is_published is True


def test_aprovar_curso_inexistente_retorna_404(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.post(f'{ADMIN_URL}00000000-0000-0000-0000-000000000000/approve/')
    assert resp.status_code == 404


def test_aprovar_retorna_campos_corretos(api_client, admin_user, pending_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.post(f'{ADMIN_URL}{pending_course.id}/approve/')
    assert set(resp.json().keys()) == {'id', 'title', 'teacher', 'status', 'is_published'}


# ── Rejeitar ───────────────────────────────────────────────────────────────


def test_anonimo_nao_pode_rejeitar(api_client, pending_course):
    resp = api_client.post(f'{ADMIN_URL}{pending_course.id}/reject/')
    assert resp.status_code == 401


def test_usuario_comum_nao_pode_rejeitar(api_client, user, pending_course):
    api_client.force_authenticate(user=user)
    resp = api_client.post(f'{ADMIN_URL}{pending_course.id}/reject/')
    assert resp.status_code == 403


def test_admin_rejeita_curso(api_client, admin_user, pending_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.post(f'{ADMIN_URL}{pending_course.id}/reject/')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'REJECTED'
    assert resp.json()['is_published'] is False


def test_rejeitar_persiste_no_banco(api_client, admin_user, pending_course):
    api_client.force_authenticate(user=admin_user)
    api_client.post(f'{ADMIN_URL}{pending_course.id}/reject/')
    pending_course.refresh_from_db()
    assert pending_course.status == 'REJECTED'
    assert pending_course.is_published is False


def test_rejeitar_curso_aprovado_despublica(api_client, admin_user, approved_course):
    api_client.force_authenticate(user=admin_user)
    api_client.post(f'{ADMIN_URL}{approved_course.id}/reject/')
    approved_course.refresh_from_db()
    assert approved_course.status == 'REJECTED'
    assert approved_course.is_published is False


def test_rejeitar_curso_inexistente_retorna_404(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.post(f'{ADMIN_URL}00000000-0000-0000-0000-000000000000/reject/')
    assert resp.status_code == 404


def test_rejeitar_retorna_campos_corretos(api_client, admin_user, pending_course):
    api_client.force_authenticate(user=admin_user)
    resp = api_client.post(f'{ADMIN_URL}{pending_course.id}/reject/')
    assert set(resp.json().keys()) == {'id', 'title', 'teacher', 'status', 'is_published'}
