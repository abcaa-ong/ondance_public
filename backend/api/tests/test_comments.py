import pytest

from course.models import Comment, Course, Lesson, Module, UserCourse
from user.models import Profile

pytestmark = pytest.mark.django_db

MODULE_DATA = {
    'title': 'Módulo 1',
    'order': 1,
}

LESSON_DATA = {
    'title': 'Aula 1 - Introdução',
    'video_url': 'https://example.com/video.mp4',
    'order': 1,
}


@pytest.fixture
def student_profile(user):
    profile, created = Profile.objects.get_or_create(user=user, defaults={'name': 'Aluno Teste'})
    if not created:
        profile.name = 'Aluno Teste'
        profile.save()
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
def module(published_course):
    return Module.objects.create(course=published_course, **MODULE_DATA)


@pytest.fixture
def lesson(module):
    return Lesson.objects.create(module=module, **LESSON_DATA)


@pytest.fixture
def enrollment(student_profile, published_course):
    return UserCourse.objects.create(profile=student_profile, course=published_course)


@pytest.fixture
def comment(student_profile, lesson, enrollment):
    return Comment.objects.create(
        profile=student_profile,
        lesson=lesson,
        content='Ótima aula!',
    )


# ── Listagem ────────────────────────────────────────────────────────────────


def test_lista_comentarios_retorna_200(api_client, lesson):
    resp = api_client.get(f'/api/lessons/{lesson.id}/comments/')
    assert resp.status_code == 200


def test_lista_comentarios_por_aula(api_client, comment, lesson):
    resp = api_client.get(f'/api/lessons/{lesson.id}/comments/')
    assert resp.status_code == 200
    assert resp.json()['count'] == 1


def test_lista_comentarios_retorna_campos_corretos(api_client, comment):
    resp = api_client.get(f'/api/lessons/{comment.lesson.id}/comments/')
    item = resp.json()['results'][0]
    assert set(item.keys()) == {
        'id', 'profile', 'lesson', 'lesson_title', 'parent', 'content',
        'student_name', 'student_photo', 'replies', 'reply_count',
        'created_at', 'updated_at',
    }


def test_student_name_retorna_nome_do_profile(api_client, comment):
    resp = api_client.get(f'/api/lessons/{comment.lesson.id}/comments/')
    assert resp.json()['results'][0]['student_name'] == 'Aluno Teste'


def test_apenas_comentarios_raiz(api_client, lesson, student_profile):
    root = Comment.objects.create(profile=student_profile, lesson=lesson, content='Pai')
    Comment.objects.create(profile=student_profile, lesson=lesson, content='Filho', parent=root)
    resp = api_client.get(f'/api/lessons/{lesson.id}/comments/')
    assert resp.json()['count'] == 1


# ── Criação ─────────────────────────────────────────────────────────────────


def test_criar_comentario_requer_autenticacao(api_client, lesson):
    resp = api_client.post(f'/api/lessons/{lesson.id}/comments/', data={
        'content': 'Teste',
    }, format='json')
    assert resp.status_code == 401


def test_criar_comentario_retorna_201(api_client, user, lesson, enrollment):
    api_client.force_authenticate(user=user)
    resp = api_client.post(f'/api/lessons/{lesson.id}/comments/', data={
        'content': 'Muito boa a aula!',
    }, format='json')
    assert resp.status_code == 201
    assert resp.json()['content'] == 'Muito boa a aula!'


def test_criar_comentario_persiste_no_banco(api_client, user, lesson, enrollment):
    api_client.force_authenticate(user=user)
    api_client.post(f'/api/lessons/{lesson.id}/comments/', data={
        'content': 'Comentário teste',
    }, format='json')
    assert Comment.objects.filter(lesson=lesson).count() == 1


def test_criar_comentario_sem_matricula_retorna_erro(api_client, user, lesson):
    api_client.force_authenticate(user=user)
    resp = api_client.post(f'/api/lessons/{lesson.id}/comments/', data={
        'content': 'Sem permissão',
    }, format='json')
    assert resp.status_code == 400


def test_criar_comentario_vazio_retorna_erro(api_client, user, lesson, enrollment):
    api_client.force_authenticate(user=user)
    resp = api_client.post(f'/api/lessons/{lesson.id}/comments/', data={
        'content': '',
    }, format='json')
    assert resp.status_code == 400


def test_criar_resposta(api_client, user, lesson, enrollment):
    api_client.force_authenticate(user=user)
    root = Comment.objects.create(
        profile=Profile.objects.get(user=user),
        lesson=lesson, content='Comentário original',
    )
    resp = api_client.post(f'/api/lessons/{lesson.id}/comments/', data={
        'content': 'Resposta',
        'parent': str(root.id),
    }, format='json')
    assert resp.status_code == 201
    assert resp.json()['parent'] == str(root.id)


def test_resposta_de_aula_diferente_retorna_erro(api_client, user, lesson, enrollment, module, published_course):
    api_client.force_authenticate(user=user)
    other_lesson = Lesson.objects.create(module=module, title='Aula 2', video_url='https://example.com/v2.mp4', order=2)
    root = Comment.objects.create(
        profile=Profile.objects.get(user=user),
        lesson=other_lesson, content='Em outra aula',
    )
    resp = api_client.post(f'/api/lessons/{lesson.id}/comments/', data={
        'content': 'Tentativa',
        'parent': str(root.id),
    }, format='json')
    assert resp.status_code == 400


# ── Atualização ─────────────────────────────────────────────────────────────


def test_atualizar_comentario_proprio(api_client, user, comment):
    api_client.force_authenticate(user=user)
    resp = api_client.patch(
        f'/api/comments/{comment.id}/',
        data={'content': 'Atualizado'},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['content'] == 'Atualizado'


def test_atualizar_comentario_de_outro_retorna_404(api_client, user, comment, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.patch(
        f'/api/comments/{comment.id}/',
        data={'content': 'Hack'},
        format='json',
    )
    assert resp.status_code == 404


# ── Deleção ─────────────────────────────────────────────────────────────────


def test_deletar_comentario_proprio(api_client, user, comment):
    api_client.force_authenticate(user=user)
    resp = api_client.delete(f'/api/comments/{comment.id}/')
    assert resp.status_code == 204
    assert not Comment.objects.filter(id=comment.id).exists()


def test_deletar_comentario_de_outro_retorna_404(api_client, user, comment, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.delete(f'/api/comments/{comment.id}/')
    assert resp.status_code == 404


# ── Replies ─────────────────────────────────────────────────────────────────


def test_respostas_aparecem_no_pai(api_client, lesson, student_profile):
    root = Comment.objects.create(profile=student_profile, lesson=lesson, content='Pai')
    Comment.objects.create(profile=student_profile, lesson=lesson, content='Filho 1', parent=root)
    Comment.objects.create(profile=student_profile, lesson=lesson, content='Filho 2', parent=root)
    resp = api_client.get(f'/api/lessons/{lesson.id}/comments/')
    item = resp.json()['results'][0]
    assert item['reply_count'] == 2
    assert len(item['replies']) == 2
