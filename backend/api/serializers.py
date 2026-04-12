import requests as http_requests

from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from course.models import Course
from user.models import City, Profile, State, User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token


class UserSerializer(serializers.ModelSerializer):
    MIN_PASSWORD_LENGTH = 8

    role = serializers.ChoiceField(
        choices=['aluno', 'professor'],
        default='aluno',
        write_only=True,
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': []},  # validate_email trata unicidade com mensagem em PT
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('E-mail já cadastrado.')
        return value

    def validate_password(self, value):
        if value is None or len(value) < self.MIN_PASSWORD_LENGTH:
            raise serializers.ValidationError(
                f'Senha deve ter pelo menos {self.MIN_PASSWORD_LENGTH} caracteres.'
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        role = validated_data.pop('role', 'aluno')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.is_teacher = (role == 'professor')
        user.is_student = (role == 'aluno')
        user.save()
        Profile.objects.create(user=user)
        return user


class PasswordChangeSerializer(serializers.Serializer):
    MIN_PASSWORD_LENGTH = 8
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Senha atual inválida.')
        return value

    def validate_new_password(self, value):
        if value is None or len(value) < self.MIN_PASSWORD_LENGTH:
            raise serializers.ValidationError(
                f'Senha deve ter pelo menos {self.MIN_PASSWORD_LENGTH} caracteres.'
            )
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'abbreviation']


class CitySerializer(serializers.ModelSerializer):
    state = serializers.SlugRelatedField(read_only=True, slug_field='abbreviation')

    class Meta:
        model = City
        fields = ['id', 'name', 'state']


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'teacher', 'is_published', 'status']
        read_only_fields = ['id', 'is_published', 'status']


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    city_detail = CitySerializer(source='city', read_only=True)
    role = serializers.ChoiceField(
        choices=['aluno', 'professor'],
        write_only=True,
        required=False,
    )

    class Meta:
        model = Profile
        fields = ['email', 'name', 'photo', 'celular', 'telephone', 'birthday', 'city', 'city_detail', 'role']
        extra_kwargs = {
            'city': {'required': False, 'allow_null': True},
            'photo': {'required': False, 'allow_null': True},
            'celular': {'required': False, 'allow_blank': True, 'allow_null': True},
            'telephone': {'required': False, 'allow_blank': True, 'allow_null': True},
            'birthday': {'required': False, 'allow_null': True},
            'name': {'required': False},
        }

    def update(self, instance, validated_data):
        role = validated_data.pop('role', None)
        if role is not None:
            instance.user.is_teacher = (role == 'professor')
            instance.user.is_student = (role == 'aluno')
            instance.user.save()
        return super().update(instance, validated_data)


GOOGLE_TOKENINFO_URL = 'https://oauth2.googleapis.com/tokeninfo'


class GoogleSocialAuthSerializer(serializers.Serializer):
    credential = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=['aluno', 'professor'],
        default='aluno',
        required=False,
    )

    def validate_credential(self, value):
        try:
            resp = http_requests.get(
                GOOGLE_TOKENINFO_URL,
                params={'id_token': value},
                timeout=5,
            )
        except http_requests.RequestException:
            raise serializers.ValidationError(
                'Não foi possível verificar o token com o Google.'
            )

        if resp.status_code != 200:
            raise serializers.ValidationError(
                'Token do Google inválido ou expirado.'
            )

        id_info = resp.json()

        if id_info.get('aud') != settings.GOOGLE_CLIENT_ID:
            raise serializers.ValidationError(
                'Token não autorizado para esta aplicação.'
            )

        if id_info.get('email_verified') != 'true':
            raise serializers.ValidationError(
                'E-mail da conta Google não verificado.'
            )

        if not id_info.get('email'):
            raise serializers.ValidationError(
                'Não foi possível obter o e-mail da conta Google.'
            )

        return id_info


# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = (
#             'id',
#             'first_name',
#             "last_name",
#             "email",
#             "national_registration",
#             "cellphone",
#             "phone",
#             "active"
#         )
