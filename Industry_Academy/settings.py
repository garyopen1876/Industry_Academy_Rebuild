"""
Django settings for Industry_Academy project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.contrib.messages import constants as messages


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(@prby^o9)he6d1#j()v@t1dis)00n3%l6b625=+6c5_^pwyfo'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

DOMAIN_NAME = ''
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
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

ROOT_URLCONF = 'Industry_Academy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'Industry_Academy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validatorsj

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

LOGGING_FOLDER = ''

# nid client_id
NID_CLIENT_ID = ''

Q_CLUSTER = {
    'name': 'DjangoORM',
    'workers': 1,
    'timeout': 1800,
    'retry': 60,
    'save_limit': 50,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}
TEST_MAIL = ''


FCU_API_CLIENT_ID = ''

try:
    from .local_settings import *
except ImportError:
    raise Exception("A local_settings.py file is required to run this project")

if LOGGING_FOLDER:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_FOLDER + '/default.log',
                'maxBytes': 1024 * 1024 * 5,  # 文件大小
                'backupCount': 0,  # 備份份數
                'formatter': 'verbose'
            },
            'request': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_FOLDER + '/request.log',
                'maxBytes': 1024 * 1024 * 5,  # 文件大小
                'backupCount': 5,  # 備份份數
                'formatter': 'verbose'
            },
            'db': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_FOLDER + '/db.log',
                'maxBytes': 1024 * 1024 * 5,  # 文件大小
                'backupCount': 1,  # 備份份數
                'formatter': 'verbose'
            },
            'template': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_FOLDER + '/template.log',
                'maxBytes': 1024 * 1024 * 5,  # 文件大小
                'backupCount': 1,  # 備份份數
                'formatter': 'verbose'
            },
            'debug': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_FOLDER + '/debug.log',
                'maxBytes': 1024 * 1024 * 5,  # 文件大小
                'backupCount': 5,  # 備份份數
                'formatter': 'verbose',
                'encoding': 'utf-8',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['default'],
                'propagate': False,
                'level': 'DEBUG',
            },
            'django.request': {
                'handlers': ['request'],
                'propagate': False,
                'level': 'DEBUG',
            },
            'django.db': {
                'handlers': ['db'],
                'propagate': False,
                'level': 'DEBUG',
            },
            'django.template': {
                'handlers': ['template'],
                'propagate': False,
                'level': 'DEBUG',
            },
            'debug': {
                'handlers': ['debug'],
                'propagate': False,
                'level': 'DEBUG',
            },
        }
    }


# postman-get-message
POSTMAN_I18N_URLS = True
POSTMAN_AUTO_MODERATE_AS = True
