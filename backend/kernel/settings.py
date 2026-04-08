from pathlib import Path
from decouple import Csv, config
from dj_database_url import parse as db_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

APPS_DEFAULT = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django.contrib.sites',
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

PERSONAL_APPS = [
    'user',
    'course',
]

INSTALLED_APPS = APPS_DEFAULT + THIRD_PARTY_APPS + PERSONAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'kernel.urls'

AUTH_USER_MODEL = 'user.User'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:9000",
]

CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kernel.wsgi.application'

default_db_url = "sqlite:///" + str(BASE_DIR / "db.sqlite3")
DATABASES = {
    "default": db_url(
        config('DATABASE_URL', default=default_db_url),
        conn_max_age=600,
        conn_health_checks=True
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'user.pagination.CustomPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
        'register': '5/minute',
        'token': '10/minute',
        'social_auth': '10/minute',
    },
    # 'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    # )
}
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'

GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', default='')

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
