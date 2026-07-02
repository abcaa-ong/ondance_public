from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

from api.serializers import (
    AdminCourseSerializer,
    AdminUserSerializer,
    CampaignSerializer,
    CertificateSerializer,
    CitySerializer,
    CommentSerializer,
    CourseDetailSerializer,
    EnrollmentSerializer,
    LeadSerializer,
    NotificationSerializer,
    ReviewSerializer,
    SaveProgressSerializer,
    StudyCourseSerializer,
    TeacherDetailSerializer,
    TeacherStudentSerializer,
    CourseSerializer,
    GoogleSocialAuthSerializer,
    PasswordChangeSerializer,
    ProfileSerializer,
    PublishedCourseSerializer,
    StateSerializer,
    UserSerializer,
)
from api.throttles import RegisterThrottle, SocialAuthThrottle
from course.models import Certificate, Comment, Course, Lesson, LessonProgress, Review, UserCourse
from user.models import Campaign, City, Lead, Notification, Profile, State, User


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = [RegisterThrottle]

    def perform_create(self, serializer):
        user = serializer.save()
        email_address = EmailAddress.objects.create(
            user=user, email=user.email, primary=True, verified=False
        )
        email_address.send_confirmation(self.request, signup=True)

create_user = UserCreate.as_view()


class CityList(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        qs = City.objects.select_related('state').order_by('name')
        state = self.request.query_params.get('state')
        if state:
            qs = qs.filter(state__abbreviation__iexact=state)
        search = self.request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(name__icontains=search)
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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = Course.objects.select_related('teacher').order_by('title')
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_published=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


courses = CourseListCreate.as_view()


class PublishedCourseList(generics.ListAPIView):
    serializer_class = PublishedCourseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        from django.db.models import Avg, Count, Q
        qs = (
            Course.objects
            .select_related('teacher__profile')
            .prefetch_related('modules')
            .filter(is_published=True)
            .annotate(
                reviews_count=Count('reviews'),
                reviews_avg=Avg('reviews__rating'),
            )
            .order_by('title')
        )

        # Filtro por estilo de dança
        dance_style = self.request.query_params.get('dance_style')
        if dance_style:
            qs = qs.filter(dance_style__iexact=dance_style)

        # Filtro por nível
        level = self.request.query_params.get('level')
        if level:
            qs = qs.filter(level__iexact=level)

        # Filtro por professor (UUID)
        teacher_id = self.request.query_params.get('teacher')
        if teacher_id:
            qs = qs.filter(teacher__id=teacher_id)

        # Filtro por carga horária (mínimo)
        workload_min = self.request.query_params.get('workload_min')
        if workload_min:
            qs = qs.filter(workload__gte=int(workload_min))

        # Filtro por carga horária (máximo)
        workload_max = self.request.query_params.get('workload_max')
        if workload_max:
            qs = qs.filter(workload__lte=int(workload_max))

        # Busca por título ou nome do professor
        search = self.request.query_params.get('search', '').strip()
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(teacher__profile__name__icontains=search) |
                Q(teacher__email__icontains=search)
            )

        return qs


published_courses = PublishedCourseList.as_view()


class TeacherCourseList(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Course.objects
            .select_related('teacher')
            .filter(teacher=self.request.user)
            .order_by('title')
        )


teacher_courses = TeacherCourseList.as_view()


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Course.objects
            .select_related('teacher')
            .prefetch_related('modules__lessons')
            .filter(teacher=self.request.user)
        )


course_detail = CourseDetail.as_view()


class AdminCourseList(generics.ListAPIView):
    serializer_class = AdminCourseSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = Course.objects.select_related('teacher__profile').order_by('title')
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        return qs


admin_course_list = AdminCourseList.as_view()


class AdminCourseApprove(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.status = 'APPROVED'
        course.is_published = True
        course.save()
        from api.notifications import notify_new_course
        notify_new_course(course)
        return Response(AdminCourseSerializer(course, context={'request': request}).data)


admin_course_approve = AdminCourseApprove.as_view()


class AdminCourseReject(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.status = 'REJECTED'
        course.is_published = False
        course.save()
        return Response(AdminCourseSerializer(course, context={'request': request}).data)


admin_course_reject = AdminCourseReject.as_view()


class AdminUserList(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = Profile.objects.select_related('user', 'city__state').filter(user__is_staff=False).order_by('name')
        role = self.request.query_params.get('role')
        if role == 'professor':
            qs = qs.filter(user__is_teacher=True)
        elif role == 'aluno':
            qs = qs.filter(user__is_teacher=False)
        search = self.request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(user__email__icontains=search)
        return qs


admin_user_list = AdminUserList.as_view()


class TeacherStudentList(generics.ListAPIView):
    serializer_class = TeacherStudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = (
            UserCourse.objects
            .select_related('profile__user', 'course')
            .filter(course__teacher=self.request.user)
            .order_by('profile__name', 'course__title')
        )
        course_id = self.request.query_params.get('course_id')
        if course_id:
            qs = qs.filter(course__id=course_id)
        return qs


teacher_students = TeacherStudentList.as_view()


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
    authentication_classes = []

    @transaction.atomic
    def post(self, request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_info = serializer.validated_data['credential']
        role = serializer.validated_data.get('role', 'aluno')
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
                user.is_teacher = (role == 'professor')
                user.is_student = (role == 'aluno')
                user.save()
                EmailAddress.objects.create(
                    user=user,
                    email=user.email,
                    primary=True,
                    verified=True,
                )
            Profile.objects.get_or_create(
                user=user,
                defaults={'name': google_name},
            )
            SocialAccount.objects.create(provider='google', uid=uid, user=user)

        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role
        refresh['name'] = user.profile.name if hasattr(user, 'profile') else ''
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'profile_complete': bool(user.profile.celular),
            },
            status=status.HTTP_200_OK,
        )


google_social_auth = GoogleSocialAuthView.as_view()


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            **serializer.data,
            'profile_complete': bool(serializer.instance.celular),
        })


profile_view = ProfileView.as_view()


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Profile.objects.select_related('user', 'city__state').order_by('name')


profile_list = ProfileListView.as_view()


class CourseEnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk, is_published=True)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        enrollment, created = UserCourse.objects.get_or_create(
            profile=profile,
            course=course,
        )
        if not created:
            return Response(
                {'message': 'Você já está matriculado neste curso.'},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = EnrollmentSerializer(enrollment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


course_enroll = CourseEnrollView.as_view()


class CourseStudyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        course = get_object_or_404(
            Course.objects.select_related('teacher__profile').prefetch_related('modules__lessons'),
            pk=pk,
            is_published=True,
        )
        profile, _ = Profile.objects.get_or_create(user=request.user)
        try:
            enrollment = UserCourse.objects.get(profile=profile, course=course)
        except UserCourse.DoesNotExist:
            return Response(
                {'message': 'Você não está matriculado neste curso.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        progress_qs = LessonProgress.objects.filter(
            user_course=enrollment
        ).select_related('lesson')
        progress_map = {str(lp.lesson_id): lp for lp in progress_qs}

        total_lessons = Lesson.objects.filter(module__course=course).count()
        completed = sum(1 for lp in progress_qs if lp.is_completed)
        progress_percent = round(completed / total_lessons * 100) if total_lessons else 0

        serializer = StudyCourseSerializer(
            course,
            context={
                'request': request,
                'progress_map': progress_map,
                'progress_percent': progress_percent,
            },
        )
        return Response(serializer.data)


course_study = CourseStudyView.as_view()


class LessonProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id, lesson_id):
        course = get_object_or_404(Course, pk=course_id)
        lesson = get_object_or_404(Lesson, pk=lesson_id)

        if not Lesson.objects.filter(pk=lesson_id, module__course=course).exists():
            return Response(
                {'message': 'Esta aula não pertence a este curso.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile, _ = Profile.objects.get_or_create(user=request.user)
        try:
            enrollment = UserCourse.objects.get(profile=profile, course=course)
        except UserCourse.DoesNotExist:
            return Response(
                {'message': 'Você não está matriculado neste curso.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SaveProgressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        progress, created = LessonProgress.objects.get_or_create(
            user_course=enrollment,
            lesson=lesson,
        )

        if 'video_position' in serializer.validated_data:
            progress.video_position = serializer.validated_data['video_position']
        if 'is_completed' in serializer.validated_data:
            progress.is_completed = serializer.validated_data['is_completed']
        progress.save()

        total_lessons = Lesson.objects.filter(module__course=course).count()
        all_completed = (
            LessonProgress.objects
            .filter(user_course=enrollment, is_completed=True)
            .count()
        )

        if total_lessons > 0 and all_completed >= total_lessons:
            from django.utils import timezone
            enrollment.is_completed = True
            enrollment.completed_at = timezone.now()
            enrollment.save()
        else:
            from api.notifications import notify_almost_done
            notify_almost_done(enrollment)

        return Response({
            'is_completed': progress.is_completed,
            'video_position': progress.video_position,
            'last_watched_at': progress.last_watched_at,
            'course_completed': enrollment.is_completed,
        })


lesson_progress = LessonProgressView.as_view()


class StudentEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return (
            UserCourse.objects
            .select_related('course__teacher__profile')
            .filter(profile=profile)
            .order_by('-started_at')
        )


student_enrollments = StudentEnrollmentsView.as_view()


class CertificateListView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return (
            Certificate.objects
            .select_related('course__teacher__profile')
            .filter(profile=profile)
            .order_by('-issue_date')
        )


certificate_list = CertificateListView.as_view()


class TeacherList(generics.ListAPIView):
    serializer_class = TeacherDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return (
            User.objects
            .filter(is_teacher=True)
            .select_related('profile')
            .order_by('profile__name')
        )


teacher_list = TeacherList.as_view()


class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = Review.objects.select_related('profile__user', 'course').order_by('-created_at')
        course_id = self.request.query_params.get('course')
        if course_id:
            qs = qs.filter(course__id=course_id)
        return qs

    def perform_create(self, serializer):
        serializer.save()


review_list_create = ReviewListCreate.as_view()


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return Review.objects.filter(profile=profile)


review_detail = ReviewDetail.as_view()


class CourseReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['pk']
        return (
            Review.objects
            .select_related('profile__user', 'course')
            .filter(course__id=course_id)
            .order_by('-created_at')
        )


course_reviews = CourseReviewsView.as_view()


class TeacherReceivedReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Review.objects
            .select_related('profile__user', 'course')
            .filter(course__teacher=self.request.user)
            .order_by('-created_at')
        )


teacher_reviews = TeacherReceivedReviewsView.as_view()


class LessonCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return (
            Comment.objects
            .select_related('profile')
            .filter(lesson__id=lesson_id, parent__isnull=True)
            .order_by('created_at')
        )

    def perform_create(self, serializer):
        lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        if not UserCourse.objects.filter(profile=profile, course=lesson.module.course).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Você precisa estar matriculado para comentar.')
        parent = serializer.validated_data.get('parent')
        if parent and parent.lesson_id != lesson.id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('O comentário pai deve pertencer à mesma aula.')
        serializer.save(lesson=lesson)


lesson_comments = LessonCommentsView.as_view()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return Comment.objects.filter(profile=profile)


comment_detail = CommentDetailView.as_view()


class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


notification_list = NotificationList.as_view()


class NotificationMarkRead(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ids = request.data.get('ids', [])
        if ids:
            Notification.objects.filter(id__in=ids, user=request.user).update(is_read=True)
        else:
            Notification.objects.filter(user=request.user).update(is_read=True)
        return Response({'ok': True})


notification_mark_read = NotificationMarkRead.as_view()


# ── Leads ───────────────────────────────────────────────────────────────────


class LeadCreate(generics.CreateAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.AllowAny]


lead_create = LeadCreate.as_view()


class LeadList(generics.ListAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Lead.objects.all()


lead_list = LeadList.as_view()


# ── Campanhas ───────────────────────────────────────────────────────────────


class CampaignListCreate(generics.ListCreateAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Campaign.objects.select_related('course', 'created_by').all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


campaign_list_create = CampaignListCreate.as_view()


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Campaign.objects.all()


campaign_detail = CampaignDetailView.as_view()


class CampaignSendView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        from django.utils import timezone
        campaign = get_object_or_404(Campaign, pk=pk)
        if campaign.status == 'sent':
            return Response({'message': 'Campanha já foi enviada.'}, status=status.HTTP_400_BAD_REQUEST)
        campaign.status = 'sent'
        campaign.sent_at = timezone.now()
        campaign.save()
        return Response(CampaignSerializer(campaign, context={'request': request}).data)


campaign_send = CampaignSendView.as_view()


# ── Analytics ───────────────────────────────────────────────────────────────


class AnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from django.db.models import Avg, Count

        total_users = User.objects.filter(is_active=True).count()
        total_students = User.objects.filter(is_student=True, is_active=True).count()
        total_teachers = User.objects.filter(is_teacher=True, is_active=True).count()
        total_courses = Course.objects.count()
        published_courses = Course.objects.filter(is_published=True).count()
        total_enrollments = UserCourse.objects.count()
        completed_enrollments = UserCourse.objects.filter(is_completed=True).count()
        total_lessons = Lesson.objects.count()

        # Cursos mais assistidos (por matrículas)
        top_courses = (
            Course.objects
            .filter(is_published=True)
            .annotate(enrollments_count=Count('usercourse'))
            .order_by('-enrollments_count')[:5]
            .values('title', 'enrollments_count')
        )

        # Tempo médio de aula (baseado em workload)
        avg_workload = Course.objects.filter(is_published=True).aggregate(
            avg=Avg('workload')
        )['avg'] or 0

        # Taxa de conclusão
        completion_rate = (
            (completed_enrollments / total_enrollments * 100)
            if total_enrollments > 0 else 0
        )

        # Média de avaliação
        avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0

        # Total de avaliações
        total_reviews = Review.objects.count()

        # Leads
        total_leads = Lead.objects.count()

        return Response({
            'total_users': total_users,
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'published_courses': published_courses,
            'total_enrollments': total_enrollments,
            'completed_enrollments': completed_enrollments,
            'total_lessons': total_lessons,
            'top_courses': list(top_courses),
            'avg_workload_hours': round(avg_workload, 1),
            'completion_rate': round(completion_rate, 1),
            'avg_rating': round(avg_rating, 1),
            'total_reviews': total_reviews,
            'total_leads': total_leads,
        })


analytics_view = AnalyticsView.as_view()
