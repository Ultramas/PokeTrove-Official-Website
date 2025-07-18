"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

from six import python_2_unicode_compatible
import django.utils.encoding

django.utils.encoding.python_2_unicode_compatible = python_2_unicode_compatible

# from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# STRIPE_PUBLIC_KEY = config('STRIPE_TEST_PUBLIC_KEY')
SECRET_KEY = 'SECRET_KEY'

SECRET = os.getenv('payment')

#stripe payment
STRIPE_KEY = 'SECRET'

# SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['54.183.195.21', 'localhost', '127.0.0.1', 'webapp-2487358.pythonanywhere.com', '*']


# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'allauth',
    "allauth.socialaccount",
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'crispy_forms',
    'crispy_bootstrap4',
    'django_private_chat2.apps.DjangoPrivateChat2Config',
    "guest_user",
    "social_django",
    'widget_tweaks',
    "guest_user.contrib.allauth",
    'changelogs',
    'favicon',
    'rest_framework',
    'sslserver',
    'showcase.apps.ShowcaseConfig',
    'user_management.apps.UserManagementConfig',
    # 'django.chatbot',
    # 'chat',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

# BACKGROUND_TASK_RUN_ASYNC = True
# CHATBOT_TEMPLATE = os.path.join(BASE_DIR, "chatbotTemplate", "webbot.template")
# START_MESSAGE = "Hello! My name is ."

# admin_interface/colorfield error command: pip install django-admin-interface (uninstalls every refresh/close)
# python manage.py loaddata admin_interface_theme_django.json

X_FRAME_OPTIONS = 'SAMEORIGIN'  # only if django version >= 3.0

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'showcase.middleware.current_room.CurrentRoomMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'showcase.middleware.middleware.CurrentUserMiddleware',
    'showcase.middleware.middleware.NotificationStatusMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'mysite.urls'

INTERNAL_IPS = [
    '127.0.0.1',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

WSGI_APPLICATION = 'mysite.wsgi.application'

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,
        },
    }
}



AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    "django.contrib.auth.backends.ModelBackend",
    "showcase.backends.UpdatedUsernameBackend",
    "guest_user.backends.GuestBackend",
]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = 'Europe/Paris'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

X_FRAME_OPTIONS = '*'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

import environ

env = environ.Env()
environ.Env.read_env()

# config/settings.py
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'  # new
# DEFAULT_FROM_EMAIL='poketrovecompany@gmail.com'
EMAIL_HOST=env('EMAIL_HOST')  # new
EMAIL_HOST_USER=env('EMAIL_HOST_USER')  # new
EMAIL_HOST_PASSWORD=env('EMAIL_HOST_PASSWORD')  # new
EMAIL_PORT=587  # new
EMAIL_USE_TLS=True  # new


# Custom setting. To email
RECIPIENT_ADDRESS = env('RECIPIENT_ADDRESS')

SECRET = os.getenv('payment')

# stripe payment
STRIPE_KEY = SECRET

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
# possibly linked to "invalid request error (invalid parameters)" issue

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
import warnings

warnings.filterwarnings(
    'error',
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r'django\.db\.models\.fields',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'


SOCIAL_AUTH_FACEBOOK_KEY = 'SOCIAL_AUTH_FACEBOOK_KEY'
SOCIAL_AUTH_FACEBOOK_SECRET = 'SOCIAL_AUTH_FACEBOOK_SECRET'

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET    = os.getenv("PAYPAL_SECRET")
PAYPAL_ENV       = "sandbox"  # or "live"


CSRF_TRUSTED_ORIGINS = [
    'http://0.0.0.0:3000',
    'http://0.0.0.0:8000',
    'http://127.0.0.1:8000',
    'https://poketrove-official-website.onrender.com',
    'https://poketrove.org',
    'https://poketrove.net',
    'https://www.poketrove.store',
    'https://poketrove.store',
]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 200000

DEFAULT_PAGINATE_BY = 10

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'