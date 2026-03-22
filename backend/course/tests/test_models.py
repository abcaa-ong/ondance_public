import pytest
from django.db import IntegrityError

from course.models import Certificate, Course

pytestmark = pytest.mark.django_db


def test_str_course_retorna_curso_de_titulo(course):
    assert str(course) == 'Curso de Ballet Clássico'


def test_novo_curso_tem_defaults_corretos(course):
    assert course.is_published is False
    assert course.status == 'PENDING'


def test_course_referencia_teacher_correto(course, teacher):
    assert course.teacher == teacher


def test_deletar_teacher_deleta_cursos_em_cascata(course, teacher):
    teacher.delete()
    assert Course.objects.count() == 0


def test_str_user_course_contem_nome_do_aluno_e_titulo_do_curso(user_course):
    assert 'Aluno Teste' in str(user_course)
    assert 'Ballet Clássico' in str(user_course)


def test_novo_progresso_tem_defaults_corretos(user_course):
    assert user_course.is_completed is False
    assert user_course.completed_at is None
    assert user_course.started_at is not None


def test_progresso_referencia_course_correto(user_course, course):
    assert user_course.course == course


def test_progresso_referencia_profile_correto(user_course, student_profile):
    assert user_course.profile == student_profile


def test_certificado_criado_com_dados_corretos(certificate):
    assert certificate.code == 'CERT-2024-001'
    assert certificate.issue_date is not None


def test_certificado_referencia_course_e_profile(certificate, course, student_profile):
    assert certificate.course == course
    assert certificate.profile == student_profile


def test_code_duplicado_em_certificate_levanta_erro(certificate, student_profile, course):
    with pytest.raises(IntegrityError):
        Certificate.objects.create(
            profile=student_profile,
            course=course,
            code='CERT-2024-001',
            file='certificates/outro.pdf',
        )
