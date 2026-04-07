from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount

from api.serializers import (
    CitySerializer,
    CourseSerializer,
    GoogleSocialAuthSerializer,
    PasswordChangeSerializer,
    StateSerializer,
    UserSerializer,
)
from api.throttles import RegisterThrottle, SocialAuthThrottle
from course.models import Course
from user.models import City, Profile, State, User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

users = UserList.as_view()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = [RegisterThrottle]

create_user = UserCreate.as_view()


class CityList(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        qs = City.objects.select_related('state').order_by('name')
        state = self.request.query_params.get('state')
        if state:
            qs = qs.filter(state__abbreviation__iexact=state)
        return qs


cities = CityList.as_view()


class StateList(generics.ListAPIView):
    serializer_class = StateSerializer

    def get_queryset(self):
        qs = State.objects.order_by('name')
        search = self.request.query_params.get('search', '').strip()
        if len(search) >= 3:
            qs = qs.filter(name__icontains=search) | qs.filter(abbreviation__icontains=search)
        return qs


states = StateList.as_view()


class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.select_related('teacher').order_by('title')
    serializer_class = CourseSerializer


courses = CourseListCreate.as_view()


class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


password_change = PasswordChangeView.as_view()


class GoogleSocialAuthView(APIView):
    throttle_classes = [SocialAuthThrottle]
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_info = serializer.validated_data['credential']
        uid = id_info['sub']
        email = User.objects.normalize_email(id_info['email'])
        google_name = id_info.get('name', '') or email.split('@')[0]

        try:
            social = SocialAccount.objects.select_related('user').get(
                provider='google', uid=uid
            )
            user = social.user
        except SocialAccount.DoesNotExist:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'email': email},
            )
            if created:
                user.set_unusable_password()
                user.save()
            Profile.objects.get_or_create(
                user=user,
                defaults={'name': google_name},
            )
            SocialAccount.objects.create(provider='google', uid=uid, user=user)

        refresh = RefreshToken.for_user(user)
        return Response(
            {'refresh': str(refresh), 'access': str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )


google_social_auth = GoogleSocialAuthView.as_view()
