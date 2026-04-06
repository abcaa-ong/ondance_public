from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views
from api.throttles import TokenThrottle


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [TokenThrottle]


urlpatterns = [
    path('register/', views.create_user, name='register'),
    path('password/change/', views.password_change, name='password_change'),
    path('courses/', views.courses, name='courses'),
    path('cities/', views.cities, name='cities'),
    path('states/', views.states, name='states'),
    path('token/', ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('rest_framework.urls', namespace='rest_framework')),
]
