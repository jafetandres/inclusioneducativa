import os
from os.path import join

import dj_database_url
from plainced.settings import *
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '0r9u3z=w6j2mq$vbus@(ppx5%f+c63pgmsnum10=!_jvl7i@2h'
DEBUG = True
ALLOWED_HOSTS = ['*']
ADMINS = [('Jafet', 'inclusioneducativa@ups.edu.ec')]

INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'social',
    'docente',
    'representante',
    'experto',
    'automata',
    'channels',
    'notifications',
    'chat',
    'multiselectfield',
    'pages'

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
ROOT_URLCONF = 'plainced.urls'

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
                'social.processors.ctx_dict',
            ],

        },
    },
]

WSGI_APPLICATION = 'plainced.wsgi.application'
ASGI_APPLICATION = 'plainced.routing.application'

# GRAPH_MODELS = {
#     'all_applications': True,
#     'group_models': True,
# }
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },

    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'plainced.db',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'plainced',
#         'USER': 'plainced',
#     }
# }

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
LANGUAGE_CODE = "es"
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_L10N = False
DATE_FORMAT = "Y-m-d"
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DATA_UPLOAD_MAX_MEMORY_SIZE = 10242880

# LOGIN_URL = '/gestionsistema/login/'
# LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = 'registration:login'
# LOGIN_REDIRECT_URL = 'registration:login'
LOGOUT_REDIRECT_URL = 'core:index'

AUTH_USER_MODEL = 'core.Usuario'

EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.ups.edu.ec'
EMAIL_HOST_USER = 'inclusioneducativa@ups.edu.ec'
EMAIL_HOST_PASSWORD = 'incluEdu2020'
EMAIL_PORT = 25
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# SECURE_HSTS_SECONDS = 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_PRELOAD = True
