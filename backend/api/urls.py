from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views
from api.serializers import CustomTokenObtainPairSerializer
from api.throttles import TokenThrottle


class ThrottledTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [TokenThrottle]


urlpatterns = [
    path('register/', views.create_user, name='register'),
    path('password/change/', views.password_change, name='password_change'),
    path('courses/', views.courses, name='courses'),
    path('courses/published/', views.published_courses, name='published-courses'),
    path('courses/mine/', views.teacher_courses, name='teacher-courses'),
    path('courses/<uuid:pk>/', views.course_detail, name='course-detail'),
    path('courses/<uuid:pk>/enroll/', views.course_enroll, name='course-enroll'),
    path('courses/<uuid:pk>/study/', views.course_study, name='course-study'),
    path('courses/<uuid:course_id>/lessons/<uuid:lesson_id>/progress/', views.lesson_progress, name='lesson-progress'),
    path('enrollments/', views.student_enrollments, name='student-enrollments'),
    path('certificates/', views.certificate_list, name='certificate-list'),
    path('admin/courses/', views.admin_course_list, name='admin-courses'),
    path('admin/courses/<uuid:pk>/approve/', views.admin_course_approve, name='admin-course-approve'),
    path('admin/courses/<uuid:pk>/reject/', views.admin_course_reject, name='admin-course-reject'),
    path('admin/users/', views.admin_user_list, name='admin-users'),
    path('teacher/students/', views.teacher_students, name='teacher-students'),
    path('teacher/reviews/', views.teacher_reviews, name='teacher-reviews'),
    path('teachers/', views.teacher_list, name='teacher-list'),
    path('reviews/', views.review_list_create, name='review-list-create'),
    path('reviews/<uuid:pk>/', views.review_detail, name='review-detail'),
    path('courses/<uuid:pk>/reviews/', views.course_reviews, name='course-reviews'),
    path('lessons/<uuid:lesson_id>/comments/', views.lesson_comments, name='lesson-comments'),
    path('comments/<uuid:pk>/', views.comment_detail, name='comment-detail'),
    path('notifications/', views.notification_list, name='notification-list'),
    path('notifications/mark-read/', views.notification_mark_read, name='notification-mark-read'),
    path('leads/', views.lead_create, name='lead-create'),
    path('admin/leads/', views.lead_list, name='lead-list'),
    path('admin/campaigns/', views.campaign_list_create, name='campaign-list-create'),
    path('admin/campaigns/<uuid:pk>/', views.campaign_detail, name='campaign-detail'),
    path('admin/campaigns/<uuid:pk>/send/', views.campaign_send, name='campaign-send'),
    path('admin/analytics/', views.analytics_view, name='analytics'),
    path('admin/dance-styles/', views.dance_style_stats, name='dance-style-stats'),
    path('admin/config/', views.platform_config, name='platform-config'),
    path('cities/', views.cities, name='cities'),
    path('states/', views.states, name='states'),
    path('auth/social/google/', views.google_social_auth, name='social_auth_google'),
    path('profile/', views.profile_view, name='profile'),
    path('profiles/', views.profile_list, name='profile-list'),
    path('token/', ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('rest_framework.urls', namespace='rest_framework')),
]
