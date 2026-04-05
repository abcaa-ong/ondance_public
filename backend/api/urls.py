from django.urls import path, include
# from rest_framework import routers

from api import views

# router = routers.DefaultRouter()

urlpatterns = [
    path('users/', views.create_user, name='users'),
    path('courses/', views.courses, name='courses'),
    path('cities/', views.cities, name='cities'),
    path('states/', views.states, name='states'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
