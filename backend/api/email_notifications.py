import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_notification_email(user, subject, template_name, context=None):
    """Send an email notification to a user."""
    if not user.email:
        return

    context = context or {}
    context['user'] = user
    context['site_name'] = 'OnDance'

    try:
        html_message = render_to_string(template_name, context)
    except Exception:
        html_message = None

    try:
        send_mail(
            subject=subject,
            message=f'Olá {user.profile.name if hasattr(user, "profile") else "Aluno"},\n\n{context.get("message", "")}',
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ondance.com',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        logger.warning(f'Failed to send email to {user.email}: {e}')


def send_new_course_email(user, course):
    """Send email when a new course is available."""
    send_notification_email(
        user=user,
        subject=f'Novo curso disponível: {course.title}',
        template_name='emails/new_course.html',
        context={
            'message': f'Um novo curso de {course.get_dance_style_display() or "dança"} está disponível!',
            'course': course,
        },
    )


def send_new_lesson_email(user, lesson, course):
    """Send email when a new lesson is available."""
    send_notification_email(
        user=user,
        subject=f'Nova aula disponível: {lesson.title}',
        template_name='emails/new_lesson.html',
        context={
            'message': f'O curso "{course.title}" tem uma nova aula.',
            'lesson': lesson,
            'course': course,
        },
    )


def send_almost_done_email(user, enrollment):
    """Send email when student is close to completing a course."""
    course = enrollment.course
    send_notification_email(
        user=user,
        subject=f'Curso quase concluído: {course.title}',
        template_name='emails/almost_done.html',
        context={
            'message': 'Você está quase lá! Continue completando as aulas restantes.',
            'course': course,
        },
    )
