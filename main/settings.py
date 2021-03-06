# coding:utf-8
"""
Django settings for hotel-api project.

Generated by 'django-admin startproject' using Django 1.10.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import datetime
from main.config import config_module
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nmd&@uy!ups^!f9)-e+8@1#9qj=4=h3tq##+*58p!)%2(!uz^t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_swagger',
    'rest_framework_jwt',
    'corsheaders',
    'django_filters',

    'main',
    'main.apps.market',
    'main.apps.hotels',
    'main.apps.admin_banner',
    'main.apps.admin_market',
    'main.apps.distribution'

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.logger.LoggerMiddleware'
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config_module.MYSQL_DB,
        'USER': config_module.MYSQL_USER,
        'PASSWORD': config_module.MYSQL_PWD,
        'HOST': config_module.MYSQL_HOST,
        'PORT': config_module.MYSQL_PORT,
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# cors header
CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = ()

# cors cookie
CORS_ALLOW_CREDENTIALS = True

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'main.common.paginator.Pagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DATETIME_INPUT_FORMATS': (
        '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
        '%Y-%m-%d',  # '2006-10-25'
        '%m/%d/%Y %H:%M:%S',  # '10/25/2006 14:30:59'
        '%m/%d/%Y %H:%M',  # '10/25/2006 14:30'
        '%m/%d/%Y',  # '10/25/2006'
        '%m/%d/%y %H:%M:%S',  # '10/25/06 14:30:59'
        '%m/%d/%y %H:%M',  # '10/25/06 14:30'
        '%m/%d/%y',  # '10/25/06'
        '%Y-%m-%dT%H:%M:%S',  # '2012-03-27T00:00:00'
        '%Y-%m-%dT%H:%M:%S.%f',  # '2012-03-27T00:00:00.000'
        '%Y-%m-%dT%H:%M:%S.%fZ',  # '2012-03-27T00:00:00.000Z'
    ),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'UNICODE_JSON': False
}

# jwt auth settings
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'main.common.jwt_response.jwt_response_payload_handler',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS512',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'jwt': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': False,
    'DOC_EXPANSION': 'list',
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/data/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/data/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'prod.info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/data/log/django.log',
        },
        'celery': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/data/log/celery.log'
        },
        'celery.error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/data/log/celery_err.log'
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'prod.info'],
            'propagate': True,
        },
        'celery': {
            'level': 'INFO',
            'handlers': ['console', 'celery', 'celery.error'],
            'propagate': True
        }
    },
}
