from django.db import transaction
from rest_framework import serializers

from course.models import Course
from user.models import City, Profile, State, User


class UserSerializer(serializers.ModelSerializer):
    MIN_PASSWORD_LENGTH = 8
    name = serializers.CharField(write_only=True)
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    celular = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'name',
            'city',
            'celular',
        ]
        extra_kwargs = {'password': {'write_only': True}}

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
        name = validated_data.pop('name')
        city = validated_data.pop('city', None)
        celular = validated_data.pop('celular', '')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        Profile.objects.create(
            user=user,
            name=name,
            city=city,
            celular=celular or None,
        )
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
