import pytest

from course.models import Course, Review, UserCourse
from user.models import Profile, User

pytestmark = pytest.mark.django_db

REVIEWS_URL = '/api/reviews/'


@pytest.fixture
def student_profile(user):
    profile, created = Profile.objects.get_or_create(user=user, defaults={'name': 'Aluno Teste'})
    if not created:
        profile.name = 'Aluno Teste'
        profile.save()
    return profile


@pytest.fixture
def teacher_profile(teacher):
    profile, _ = Profile.objects.get_or_create(user=teacher, defaults={'name': 'Prof. Ana'})
    return profile


@pytest.fixture
def published_course(teacher):
    return Course.objects.create(
        title='Ballet Clássico',
        teacher=teacher,
        status='APPROVED',
        is_published=True,
    )


@pytest.fixture
def enrollment(student_profile, published_course):
    return UserCourse.objects.create(profile=student_profile, course=published_course)


@pytest.fixture
def review(student_profile, published_course, enrollment):
    return Review.objects.create(
        profile=student_profile,
        course=published_course,
        rating=5,
        comment='Excelente curso!',
    )


# ── Listagem ────────────────────────────────────────────────────────────────


def test_lista_avaliacoes_retorna_200(api_client):
    resp = api_client.get(REVIEWS_URL)
    assert resp.status_code == 200


def test_lista_avaliacoes_por_curso(api_client, review, published_course):
    resp = api_client.get(REVIEWS_URL, {'course': published_course.id})
    assert resp.status_code == 200
    assert resp.json()['count'] == 1


def test_lista_avaliacoes_retorna_campos_corretos(api_client, review):
    resp = api_client.get(REVIEWS_URL)
    item = resp.json()['results'][0]
    assert set(item.keys()) == {
        'id', 'profile', 'course', 'course_title', 'rating', 'comment',
        'student_name', 'student_photo', 'created_at', 'updated_at',
    }


def test_student_name_retorna_nome_do_profile(api_client, review):
    resp = api_client.get(REVIEWS_URL)
    assert resp.json()['results'][0]['student_name'] == 'Aluno Teste'


def test_course_title_retorna_titulo_do_curso(api_client, review):
    resp = api_client.get(REVIEWS_URL)
    assert resp.json()['results'][0]['course_title'] == 'Ballet Clássico'


# ── Criação ─────────────────────────────────────────────────────────────────


def test_criar_avaliacao_requer_autenticacao(api_client, published_course):
    resp = api_client.post(REVIEWS_URL, data={
        'course': str(published_course.id),
        'rating': 4,
    }, format='json')
    assert resp.status_code == 401


def test_criar_avaliacao_retorna_201(api_client, user, published_course, enrollment):
    api_client.force_authenticate(user=user)
    resp = api_client.post(REVIEWS_URL, data={
        'course': str(published_course.id),
        'rating': 5,
        'comment': 'Muito bom!',
    }, format='json')
    assert resp.status_code == 201
    assert resp.json()['rating'] == 5
    assert resp.json()['comment'] == 'Muito bom!'


def test_criar_avaliacao_persiste_no_banco(api_client, user, published_course, enrollment):
    api_client.force_authenticate(user=user)
    api_client.post(REVIEWS_URL, data={
        'course': str(published_course.id),
        'rating': 4,
    }, format='json')
    assert Review.objects.filter(course=published_course).count() == 1


def test_criar_avaliacao_sem_matricula_retorna_erro(api_client, user, published_course):
    api_client.force_authenticate(user=user)
    resp = api_client.post(REVIEWS_URL, data={
        'course': str(published_course.id),
        'rating': 5,
    }, format='json')
    assert resp.status_code == 400


def test_criar_avaliacao_nota_invalida_retorna_erro(api_client, user, published_course, enrollment):
    api_client.force_authenticate(user=user)
    resp = api_client.post(REVIEWS_URL, data={
        'course': str(published_course.id),
        'rating': 6,
    }, format='json')
    assert resp.status_code == 400


def test_criar_avaliacao_nota_zero_retorna_erro(api_client, user, published_course, enrollment):
    api_client.force_authenticate(user=user)
    resp = api_client.post(REVIEWS_URL, data={
        'course': str(published_course.id),
        'rating': 0,
    }, format='json')
    assert resp.status_code == 400


def test_criar_avaliacao_duplicada_retorna_erro(api_client, user, published_course, enrollment, review):
    api_client.force_authenticate(user=user)
    resp = api_client.post(REVIEWS_URL, data={
        'course': str(published_course.id),
        'rating': 3,
    }, format='json')
    assert resp.status_code == 400


# ── Atualização ─────────────────────────────────────────────────────────────


def test_atualizar_avaliacao_propria(api_client, user, review):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(
        f'{REVIEWS_URL}{review.id}/',
        data={'rating': 4, 'comment': 'Atualizado'},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['rating'] == 4
    assert resp.json()['comment'] == 'Atualizado'


def test_atualizar_avaliacao_de_outro_retorna_404(api_client, user, review, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.patch(
        f'{REVIEWS_URL}{review.id}/',
        data={'rating': 1},
        format='json',
    )
    assert resp.status_code == 404


# ── Deleção ─────────────────────────────────────────────────────────────────


def test_deletar_avaliacao_propria(api_client, user, review):
    api_client.force_authenticate(user=user)
    resp = api_client.delete(f'{REVIEWS_URL}{review.id}/')
    assert resp.status_code == 204
    assert not Review.objects.filter(id=review.id).exists()


def test_deletar_avaliacao_de_outro_retorna_404(api_client, user, review, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.delete(f'{REVIEWS_URL}{review.id}/')
    assert resp.status_code == 404


# ── Avaliações por curso ────────────────────────────────────────────────────


def test_avaliacoes_por_curso_retorna_200(api_client, review, published_course):
    resp = api_client.get(f'/api/courses/{published_course.id}/reviews/')
    assert resp.status_code == 200
    assert resp.json()['count'] == 1


def test_avaliacoes_por_curso_sem_avaliacoes(api_client, published_course):
    resp = api_client.get(f'/api/courses/{published_course.id}/reviews/')
    assert resp.status_code == 200
    assert resp.json()['count'] == 0


# ── Avaliações do professor ─────────────────────────────────────────────────


def test_professor_ve_avaliacoes_recebidas(api_client, teacher, review):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get('/api/teacher/reviews/')
    assert resp.status_code == 200
    assert resp.json()['count'] == 1


def test_professor_nao_ve_avaliacoes_de_outros(api_client, teacher, user, published_course):
    other_teacher = User.objects.create_user(email='outro@teste.com', password='senha123')
    other_course = Course.objects.create(
        title='Outro Curso', teacher=other_teacher, is_published=True
    )
    other_profile, _ = Profile.objects.get_or_create(user=user, defaults={'name': 'Aluno Outro'})
    UserCourse.objects.create(profile=other_profile, course=other_course)
    Review.objects.create(profile=other_profile, course=other_course, rating=3)

    api_client.force_authenticate(user=teacher)
    resp = api_client.get('/api/teacher/reviews/')
    assert resp.json()['count'] == 0
