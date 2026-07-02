from user.models import Notification


def notify_new_lesson(lesson):
    """Notify enrolled students when a new lesson is added."""
    from course.models import UserCourse
    course = lesson.module.course
    enrollments = UserCourse.objects.filter(course=course).select_related('profile__user')
    for enrollment in enrollments:
        Notification.objects.create(
            user=enrollment.profile.user,
            type='new_lesson',
            title=f'Nova aula disponível: {lesson.title}',
            message=f'O curso "{course.title}" tem uma nova aula.',
            link=f'/student/courses/{course.id}/assistir',
        )
        from api.email_notifications import send_new_lesson_email
        send_new_lesson_email(enrollment.profile.user, lesson, course)


def notify_new_course(course):
    """Notify all students when a new course is published."""
    from user.models import User
    students = User.objects.filter(is_student=True, is_active=True)
    for student in students:
        Notification.objects.create(
            user=student,
            type='new_course',
            title=f'Novo curso: {course.title}',
            message=f'Um novo curso de {course.get_dance_style_display() or "dança"} está disponível!',
            link='/student/explorar',
        )
        from api.email_notifications import send_new_course_email
        send_new_course_email(student, course)


def notify_almost_done(enrollment):
    """Notify student when they're close to completing a course."""
    course = enrollment.course
    total = sum(m.lessons.count() for m in course.modules.all())
    if total == 0:
        return
    completed = sum(
        1 for m in course.modules.all()
        for lesson in m.lessons.all()
        if hasattr(lesson, 'progress') and lesson.progress.filter(profile=enrollment.profile, is_completed=True).exists()
    )
    percent = int((completed / total) * 100)
    if percent >= 80 and not Notification.objects.filter(
        user=enrollment.profile.user, type='almost_done',
        title__contains=course.title,
    ).exists():
        Notification.objects.create(
            user=enrollment.profile.user,
            type='almost_done',
            title=f'Curso quase concluído: {course.title}',
            message=f'Você já completou {percent}% do curso. Continue!',
            link=f'/student/courses/{course.id}/assistir',
        )
        from api.email_notifications import send_almost_done_email
        send_almost_done_email(enrollment.profile.user, enrollment)
