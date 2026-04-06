from django.db import transaction
from rest_framework import serializers

from course.models import Course
from user.models import City, Profile, State, User


class UserSerializer(serializers.ModelSerializer):
    MIN_PASSWORD_LENGTH = 8

    class Meta:
        model = User
        fields = ['id', 'email', 'password']
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
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
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
