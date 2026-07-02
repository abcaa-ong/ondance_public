import pytest

from course.models import Course, Lesson, Module

pytestmark = pytest.mark.django_db

COURSES_URL = '/api/courses/'


@pytest.fixture
def course_with_modules(teacher):
    course = Course.objects.create(title='Ballet Completo', teacher=teacher)
    mod1 = Module.objects.create(course=course, title='Módulo 1', order=0)
    Module.objects.create(course=course, title='Módulo 2', order=1)
    Lesson.objects.create(module=mod1, title='Aula 1', order=0)
    Lesson.objects.create(module=mod1, title='Aula 2', order=1)
    return course


# ── Criação com modules ────────────────────────────────────────────────────


def test_cria_course_com_modules_e_lessons(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    payload = {
        'title': 'Samba Avançado',
        'description': 'Curso completo de samba',
        'duration': '6 semanas',
        'level': 'Avançado',
        'modules': [
            {
                'title': 'Fundamentos',
                'order': 0,
                'lessons': [
                    {'title': 'Introdução', 'order': 0},
                    {'title': 'Passos básicos', 'order': 1},
                ],
            },
            {
                'title': 'Avançado',
                'order': 1,
                'lessons': [
                    {'title': 'Giros', 'order': 0},
                ],
            },
        ],
    }
    resp = api_client.post(COURSES_URL, data=payload, format='json')
    assert resp.status_code == 201
    body = resp.json()
    assert body['title'] == 'Samba Avançado'
    assert body['description'] == 'Curso completo de samba'
    assert body['duration'] == '6 semanas'
    assert body['level'] == 'Avançado'
    assert len(body['modules']) == 2
    assert len(body['modules'][0]['lessons']) == 2
    assert len(body['modules'][1]['lessons']) == 1


def test_cria_course_sem_modules_funciona(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    resp = api_client.post(COURSES_URL, data={'title': 'Solo'}, format='json')
    assert resp.status_code == 201
    assert resp.json()['modules'] == []


# ── Detail com modules ─────────────────────────────────────────────────────


def test_detail_retorna_modules_e_lessons(api_client, teacher, course_with_modules):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(f'{COURSES_URL}{course_with_modules.id}/')
    assert resp.status_code == 200
    body = resp.json()
    assert len(body['modules']) == 2
    assert body['modules'][0]['title'] == 'Módulo 1'
    assert len(body['modules'][0]['lessons']) == 2


def test_detail_retorna_campos_do_curso(api_client, teacher, course_with_modules):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(f'{COURSES_URL}{course_with_modules.id}/')
    body = resp.json()
    assert 'title' in body
    assert 'description' in body
    assert 'modules' in body


# ── Update com modules ─────────────────────────────────────────────────────


def test_atualiza_titulo_do_curso(api_client, teacher, course_with_modules):
    api_client.force_authenticate(user=teacher)
    resp = api_client.patch(
        f'{COURSES_URL}{course_with_modules.id}/',
        data={'title': 'Novo Título'},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['title'] == 'Novo Título'


def test_adiciona_novo_module_no_update(api_client, teacher, course_with_modules):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(f'{COURSES_URL}{course_with_modules.id}/')
    modules = resp.json()['modules']
    modules.append({
        'title': 'Módulo 3',
        'order': 2,
        'lessons': [{'title': 'Aula nova', 'order': 0}],
    })
    resp = api_client.put(
        f'{COURSES_URL}{course_with_modules.id}/',
        data={'title': course_with_modules.title, 'modules': modules},
        format='json',
    )
    assert resp.status_code == 200
    assert len(resp.json()['modules']) == 3


def test_remove_module_no_update(api_client, teacher, course_with_modules):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(f'{COURSES_URL}{course_with_modules.id}/')
    modules = resp.json()['modules'][:1]  # mantém só o primeiro
    resp = api_client.put(
        f'{COURSES_URL}{course_with_modules.id}/',
        data={'title': course_with_modules.title, 'modules': modules},
        format='json',
    )
    assert resp.status_code == 200
    assert len(resp.json()['modules']) == 1


def test_atualiza_titulo_da_lesson(api_client, teacher, course_with_modules):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(f'{COURSES_URL}{course_with_modules.id}/')
    modules = resp.json()['modules']
    modules[0]['lessons'][0]['title'] = 'Aula renomeada'
    resp = api_client.put(
        f'{COURSES_URL}{course_with_modules.id}/',
        data={'title': course_with_modules.title, 'modules': modules},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['modules'][0]['lessons'][0]['title'] == 'Aula renomeada'


def test_remove_lesson_no_update(api_client, teacher, course_with_modules):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(f'{COURSES_URL}{course_with_modules.id}/')
    modules = resp.json()['modules']
    modules[0]['lessons'] = []  # remove todas as aulas do primeiro módulo
    resp = api_client.put(
        f'{COURSES_URL}{course_with_modules.id}/',
        data={'title': course_with_modules.title, 'modules': modules},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['modules'][0]['lessons'] == []


# ── Counts ─────────────────────────────────────────────────────────────────


def test_modules_count_e_lessons_count(api_client, teacher, course_with_modules):
    # course_with_modules tem 2 módulos e 2 aulas
    api_client.force_authenticate(user=teacher)
    resp = api_client.get('/api/courses/mine/')
    cursos = resp.json()['results']
    curso = next(c for c in cursos if c['id'] == str(course_with_modules.id))
    assert curso['modules_count'] == 2
    assert curso['lessons_count'] == 2


# ── Exercises ───────────────────────────────────────────────────────────────


def test_cria_lesson_com_exercises(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    payload = {
        'title': 'Zouk',
        'modules': [
            {
                'title': 'Módulo 1',
                'order': 0,
                'lessons': [
                    {
                        'title': 'Aula com exercícios',
                        'order': 0,
                        'exercises': 'Pratique o passo básico 10 vezes',
                    },
                ],
            },
        ],
    }
    resp = api_client.post(COURSES_URL, data=payload, format='json')
    assert resp.status_code == 201
    lesson = resp.json()['modules'][0]['lessons'][0]
    assert lesson['exercises'] == 'Pratique o passo básico 10 vezes'


def test_exercises_default_vazio(api_client, teacher):
    api_client.force_authenticate(user=teacher)
    payload = {
        'title': 'Samba',
        'modules': [
            {
                'title': 'Módulo 1',
                'order': 0,
                'lessons': [{'title': 'Aula sem exercícios', 'order': 0}],
            },
        ],
    }
    resp = api_client.post(COURSES_URL, data=payload, format='json')
    assert resp.status_code == 201
    lesson = resp.json()['modules'][0]['lessons'][0]
    assert lesson['exercises'] == ''


def test_atualiza_exercises_da_lesson(api_client, teacher, course_with_modules):
    api_client.force_authenticate(user=teacher)
    resp = api_client.get(f'{COURSES_URL}{course_with_modules.id}/')
    modules = resp.json()['modules']
    modules[0]['lessons'][0]['exercises'] = 'Faça 5 séries de alongamento'
    resp = api_client.put(
        f'{COURSES_URL}{course_with_modules.id}/',
        data={'title': course_with_modules.title, 'modules': modules},
        format='json',
    )
    assert resp.status_code == 200
    assert resp.json()['modules'][0]['lessons'][0]['exercises'] == 'Faça 5 séries de alongamento'


def test_study_retorna_exercises(api_client, user, teacher):
    from course.models import UserCourse
    from user.models import Profile

    api_client.force_authenticate(user=teacher)
    course = Course.objects.create(title='Forró', teacher=teacher, is_published=True)
    mod = Module.objects.create(course=course, title='Módulo 1', order=0)
    Lesson.objects.create(
        module=mod,
        title='Aula 1',
        order=0,
        exercises='Pratique o balanço do corpo',
    )
    profile, _ = Profile.objects.get_or_create(user=user)
    UserCourse.objects.create(profile=profile, course=course)
    api_client.force_authenticate(user=user)
    resp = api_client.get(f'{COURSES_URL}{course.id}/study/')
    assert resp.status_code == 200
    lesson = resp.json()['modules'][0]['lessons'][0]
    assert lesson['exercises'] == 'Pratique o balanço do corpo'
