import pytest

from course.models import Course

pytestmark = pytest.mark.django_db

COURSES_URL = '/api/courses/'


# ── Listagem (GET) ─────────────────────────────────────────────────────────


def test_lista_courses_retorna_200(api_client, published_course):
    resp = api_client.get(COURSES_URL)
    assert resp.status_code == 200


def test_lista_courses_retorna_campos_corretos(api_client, published_course):
    resp = api_client.get(COURSES_URL)
    primeiro = resp.json()['results'][0]
    assert set(primeiro.keys()) == {
        'id', 'title', 'description', 'duration', 'level', 'workload',
        'dance_style', 'emoji', 'thumb_bg', 'teacher', 'is_published', 'status',
        'modules_count', 'lessons_count',
    }


def test_lista_courses_em_ordem_alfabetica(api_client, teacher):
    Course.objects.create(title='Zouk', teacher=teacher, is_published=True)
    Course.objects.create(title='Ballet', teacher=teacher, is_published=True)
    resp = api_client.get(COURSES_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert titulos == sorted(titulos)


def test_teacher_no_response_e_email(api_client, published_course, teacher):
    resp = api_client.get(COURSES_URL)
    assert resp.json()['results'][0]['teacher'] == teacher.email


# ── Visibilidade anônimo vs. autenticado ───────────────────────────────────


def test_anonimo_so_ve_cursos_publicados(api_client, published_course, draft_course):
    resp = api_client.get(COURSES_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert published_course.title in titulos
    assert draft_course.title not in titulos


def test_anonimo_nao_ve_cursos_em_rascunho(api_client, draft_course):
    resp = api_client.get(COURSES_URL)
    assert resp.json()['results'] == []


def test_autenticado_ve_todos_os_cursos(api_client, user, published_course, draft_course):
    api_client.force_authenticate(user=user)
    resp = api_client.get(COURSES_URL)
    titulos = [c['title'] for c in resp.json()['results']]
    assert published_course.title in titulos
    assert draft_course.title in titulos


def test_autenticado_ve_cursos_nao_publicados(api_client, user, draft_course):
    api_client.force_authenticate(user=user)
    resp = api_client.get(COURSES_URL)
    assert resp.json()['results'][0]['title'] == draft_course.title


# ── Criação (POST) ─────────────────────────────────────────────────────────


def test_post_requer_autenticacao(api_client):
    resp = api_client.post(COURSES_URL, data={'title': 'Contemporâneo'}, format='json')
    assert resp.status_code == 401


def test_cria_course_com_defaults(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.post(COURSES_URL, data={'title': 'Contemporâneo'}, format='json')
    assert resp.status_code == 201
    body = resp.json()
    assert body['title'] == 'Contemporâneo'
    assert body['teacher']['email'] == teacher.email
    assert body['is_published'] is False
    assert body['status'] == 'PENDING'


def test_cria_course_persiste_no_banco(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    api_client.post(COURSES_URL, data={'title': 'Forró Universitário'}, format='json')
    assert Course.objects.filter(title='Forró Universitário').exists()


def test_post_sem_title_retorna_400(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.post(COURSES_URL, data={}, format='json')
    assert resp.status_code == 400


# ── Workload (carga horária) ────────────────────────────────────────────────


def test_cria_course_com_workload(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.post(COURSES_URL, data={'title': 'Ballet', 'workload': 40}, format='json')
    assert resp.status_code == 201
    assert resp.json()['workload'] == 40


def test_workload_default_zero(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.post(COURSES_URL, data={'title': 'Jazz'}, format='json')
    assert resp.status_code == 201
    assert resp.json()['workload'] == 0


def test_atualiza_workload_via_patch(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.patch(
        f'{COURSES_URL}{published_course.id}/',
        data={'workload': 60},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['workload'] == 60
    published_course.refresh_from_db()
    assert published_course.workload == 60
