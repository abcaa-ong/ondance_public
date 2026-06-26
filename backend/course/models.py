import uuid

from django.db import models

from user.models import Profile, User


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    duration = models.CharField(max_length=50, blank=True, default='')
    level = models.CharField(max_length=20, blank=True, default='')
    emoji = models.CharField(max_length=10, blank=True, default='')
    thumb_bg = models.CharField(max_length=7, blank=True, default='')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='PENDING')

    def __str__(self):
        return f"Curso de {self.title}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['title']


class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Módulo {self.order + 1}: {self.title}"

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ['order', 'title']


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, default='')
    content = models.TextField(blank=True, default='')
    materials_url = models.URLField(blank=True, default='')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Aula {self.order + 1}: {self.title}"

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        ordering = ['order', 'title']


class UserCourse(models.Model):
    """Tabela intermediária para controlar o progresso"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Progresso de {self.profile.name} em {self.course.title}"

    class Meta:
        verbose_name = "Progresso"
        verbose_name_plural = "Progressos"
        ordering = ['-started_at']


class LessonProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_entries')
    is_completed = models.BooleanField(default=False)
    video_position = models.PositiveIntegerField(default=0)
    last_watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Progresso da Aula"
        verbose_name_plural = "Progressos das Aulas"
        constraints = [
            models.UniqueConstraint(fields=['user_course', 'lesson'], name='unique_lesson_progress'),
        ]

    def __str__(self):
        status = 'concluída' if self.is_completed else f'{self.video_position}s'
        return f"{self.user_course.profile.name} — {self.lesson.title} ({status})"


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    code = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f"Certificado de {self.profile.name} — {self.course.title}"

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
