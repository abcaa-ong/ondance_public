import pytest

from course.models import Course
from user.models import User

pytestmark = pytest.mark.django_db

DETAIL_URL = '/api/courses/{}/'


@pytest.fixture
def other_teacher(db):
    return User.objects.create_user(email='outro@teste.com', password='senha123')


@pytest.fixture
def other_course(other_teacher):
    return Course.objects.create(title='Forró', teacher=other_teacher)


# ── GET (retrieve) ─────────────────────────────────────────────────────────


def test_get_anonimo_recebe_401(api_client, published_course):
    resp = api_client.get(DETAIL_URL.format(published_course.id))
    assert resp.status_code == 401


def test_get_dono_recebe_200(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(DETAIL_URL.format(published_course.id))
    assert resp.status_code == 200


def test_get_retorna_campos_corretos(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(DETAIL_URL.format(published_course.id))
    assert set(resp.json().keys()) == {'id', 'title', 'teacher', 'is_published', 'status'}


def test_get_retorna_dados_do_curso(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(DETAIL_URL.format(published_course.id))
    body = resp.json()
    assert body['title'] == published_course.title
    assert body['teacher'] == teacher.email


def test_get_curso_de_outro_professor_retorna_404(api_client, teacher, other_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(DETAIL_URL.format(other_course.id))
    assert resp.status_code == 404


def test_get_uuid_inexistente_retorna_404(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(DETAIL_URL.format('00000000-0000-0000-0000-000000000000'))
    assert resp.status_code == 404


# ── PUT (full update) ──────────────────────────────────────────────────────


def test_put_anonimo_recebe_401(api_client, published_course):
    resp = api_client.put(
        DETAIL_URL.format(published_course.id),
        data={'title': 'Novo Título'},
        format='json',
    )
    assert resp.status_code == 401


def test_put_dono_atualiza_titulo(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.put(
        DETAIL_URL.format(published_course.id),
        data={'title': 'Ballet Moderno'},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['title'] == 'Ballet Moderno'


def test_put_persiste_no_banco(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    api_client.put(
        DETAIL_URL.format(published_course.id),
        data={'title': 'Ballet Moderno'},
        format='json',
    )
    published_course.refresh_from_db()
    assert published_course.title == 'Ballet Moderno'


def test_put_sem_title_retorna_400(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.put(
        DETAIL_URL.format(published_course.id),
        data={},
        format='json',
    )
    assert resp.status_code == 400


def test_put_curso_de_outro_professor_retorna_404(api_client, teacher, other_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.put(
        DETAIL_URL.format(other_course.id),
        data={'title': 'Invasão'},
        format='json',
    )
    assert resp.status_code == 404


def test_put_nao_altera_teacher_nem_status(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.put(
        DETAIL_URL.format(published_course.id),
        data={'title': 'Ballet Moderno', 'status': 'APPROVED', 'is_published': True},
        format='json',
    )
    body = resp.json()
    assert body['status'] == 'PENDING'
    assert body['is_published'] is True  # is_published permanece inalterado (read_only)
    assert body['teacher'] == teacher.email


# ── PATCH (partial update) ─────────────────────────────────────────────────


def test_patch_anonimo_recebe_401(api_client, published_course):
    resp = api_client.patch(
        DETAIL_URL.format(published_course.id),
        data={'title': 'Novo'},
        format='json',
    )
    assert resp.status_code == 401


def test_patch_dono_atualiza_titulo(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.patch(
        DETAIL_URL.format(published_course.id),
        data={'title': 'Ballet Contemporâneo'},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['title'] == 'Ballet Contemporâneo'


def test_patch_curso_de_outro_professor_retorna_404(api_client, teacher, other_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.patch(
        DETAIL_URL.format(other_course.id),
        data={'title': 'Invasão'},
        format='json',
    )
    assert resp.status_code == 404


# ── DELETE ─────────────────────────────────────────────────────────────────


def test_delete_anonimo_recebe_401(api_client, published_course):
    resp = api_client.delete(DETAIL_URL.format(published_course.id))
    assert resp.status_code == 401


def test_delete_dono_recebe_204(api_client, teacher, published_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.delete(DETAIL_URL.format(published_course.id))
    assert resp.status_code == 204


def test_delete_remove_do_banco(api_client, teacher, published_course):
    course_id = published_course.id
    api_client.force_authenticate(user=teacher)
    api_client.delete(DETAIL_URL.format(course_id))
    assert not Course.objects.filter(id=course_id).exists()


def test_delete_curso_de_outro_professor_retorna_404(api_client, teacher, other_course):
    api_client.force_authenticate(user=teacher)
    resp = api_client.delete(DETAIL_URL.format(other_course.id))
    assert resp.status_code == 404
