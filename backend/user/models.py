import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'  # Define o e-mail como login
    REQUIRED_FIELDS = []      # O email já é obrigatório por ser USERNAME_FIELD

    def __str__(self):
        return self.email


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    celular = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.name}"


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2, unique=True)  # Ex: SP, RJ

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.name} - {self.state.abbreviation}"
