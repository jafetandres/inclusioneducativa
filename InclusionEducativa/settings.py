"""
Django settings for InclusionEducativa project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from InclusionEducativa.settings import *
import os
import dj_database_url
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0r9u3z=w6j2mq$vbus@(ppx5%f+c63pgmsnum10=!_jvl7i@2h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# DEBUG = False
#
# ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'InclusionEducativa.Apps.GestionSistema',
    'InclusionEducativa.Apps.AppDocente',
    'InclusionEducativa.Apps.AppRepresentante',
    'InclusionEducativa.Apps.AppExperto',
    'pwa',
    'django_chatter',
    'channels',
    'notifications',
    'django_summernote'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'InclusionEducativa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'InclusionEducativa/templates')],
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

# CHATTER_BASE_TEMPLATE ='Chat/base.html'

WSGI_APPLICATION = 'InclusionEducativa.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'InclusionEducativa.db',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'inclusioneducativa',
#         'USER': 'postgres',
#         'PASSWORD': '1234',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)


ASGI_APPLICATION = 'InclusionEducativa.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },

    },
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
LANGUAGE_CODE = "es-es"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

DATE_FORMAT = "Y-m-d"

USE_TZ = True

# STATIC_ROOT = "InclusionEducativa/static"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
#     '/var/www/static/',
# ]

STATIC_URL = '/static/'

STATICFILES_DIRS = [(os.path.join(BASE_DIR, 'InclusionEducativa/static/')), ]
#
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


AUTH_USER_MODEL = 'GestionSistema.Usuario'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jafetgalvez1@gmail.com'
EMAIL_HOST_PASSWORD = 'kgelhlrlozgcpoum'
EMAIL_PORT = 587
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'InclusionEducativa/media')
DATA_UPLOAD_MAX_MEMORY_SIZE = 10242880
