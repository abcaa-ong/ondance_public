import pytest

from course.models import Certificate, Course, UserCourse
from user.models import City, Profile, State, User


@pytest.fixture
def state(db):
    return State.objects.create(name='São Paulo', abbreviation='SP')


@pytest.fixture
def city(state):
    return City.objects.create(name='Campinas', state=state)


@pytest.fixture
def teacher(db):
    user = User.objects.create_user(email='professor@teste.com', password='senha123')
    user.is_teacher = True
    user.is_student = False
    user.save()
    return user


@pytest.fixture
def student(db):
    return User.objects.create_user(email='aluno@teste.com', password='senha123')


@pytest.fixture
def student_profile(student, city):
    return Profile.objects.create(
        user=student,
        name='Aluno Teste',
        city=city,
        celular='11988888888',
    )


@pytest.fixture
def course(teacher):
    return Course.objects.create(title='Ballet Clássico', teacher=teacher)


@pytest.fixture
def user_course(student_profile, course):
    return UserCourse.objects.create(profile=student_profile, course=course)


@pytest.fixture
def certificate(student_profile, course):
    return Certificate.objects.create(
        profile=student_profile,
        course=course,
        code='CERT-2024-001',
        file='certificates/cert.pdf',
    )
