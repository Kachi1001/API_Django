"""
Django settings for site_django project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hss4fba%6y**i6$hkin&j@gp3h^^7r5*duji$-f1&(_#m6*gx#'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DJ_DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = config("DJ_ALLOWED_HOSTS", default="10.0.0.139").split(",")



# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    ]

INTERNAL_APP = []
for app in BASE_DIR.iterdir():
    app = app.stem
    if os.path.exists('/'.join([str(BASE_DIR),app,'urls.py'])) and app != 'Site_django':
        INTERNAL_APP.append(str(app))
            
INSTALLED_APPS += INTERNAL_APP

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:80",  # Domínio que está fazendo a requisição
    "http://10.0.0.139:80", # Produção
    "http://10.0.0.139:81", # Teste
    "http://10.0.0.211:81" # Debug
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
ROOT_URLCONF = 'Site_django.urls'

TEMPLATES = []

WSGI_APPLICATION = 'Site_django.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Inclua o caminho dos seus templates aqui, se necessário
        ],
        'APP_DIRS': True,  # Certifique-se de que isto está ativado
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
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASE_ROUTERS = ['Site_django.routers.AppRouter']
DATABASES = {}

for app in INTERNAL_APP:
    db = app
    if app == "Home":
        app = 'default'
        db = 'Site_Django'
    DATABASES[app]  = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db,
        "USER": config("DB_USER", "django"),
        "PASSWORD": config("DB_PASSWORD", 'django@senha'),
        "HOST": config("DB_HOST", '127.0.0.1'),
        "PORT": config("DB_PORT", '5432'),
    }
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'
DATE_INPUT_FORMATS = '%m/%d/%Y'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT= config('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://10.0.0.139:6379/1',  # Use o endereço do Redis
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'KEY_PREFIX': '',
            'VERSION': 0
        }
    }
}
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication')
}

import logging

# # Configuração do logger
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'simple': {
#             'format': '%(levelname)s: %(message)s',  # Formato simples sem traceback
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'ERROR',  # Nível do log
#         },
#         '': {  # Logger raiz
#             'handlers': ['console'],
#             'level': 'ERROR',  # Nível do log
#         },
#     },
# }
APPEND_SLASH = True
