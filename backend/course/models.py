from django.db import models

from user.models import Profile, User


class Course(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False) # Só o Admin ou Professor mudam
    status = models.CharField(max_length=20, default='PENDING') # PENDING, APPROVED, REJECTED

    def __str__(self):
        return f"Curso de {self.title}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['title']


class UserCourse(models.Model):
    """ Tabela intermediária para controlar o progresso """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Certificado de {self.profile.user.name} para {self.course.title}"

    class Meta:
        verbose_name = "Progresso"
        verbose_name_plural = "Progressos"
        ordering = ['-started_at']


class Certificate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    code = models.CharField(max_length=100, unique=True) # Código de validação
    file = models.FileField(upload_to='certificates/')
