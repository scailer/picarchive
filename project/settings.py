# -*- coding: utf-8 -*-

import os
import sys
import djcelery
from django.core.exceptions import ImproperlyConfigured

djcelery.setup_loader()

IS_TESTING = bool(('test' in sys.argv) or ('test_coverage' in sys.argv))
IS_LOADDATA = bool('loaddata' in sys.argv)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
PROJECT_NAME = 'picarchive'

ADMINS = (
    ('Vlasov Dmitry', 'scailer@veles.biz'),
)

MANAGERS = ADMINS

AUTH_USER_MODEL = 'account.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'project/picarchive.db',
    }
}

APPEND_SLASH=False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

USE_TZ = True
TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru'
USE_I18N = True
USE_L10N = True
SITE_ID = 1

_ = lambda s: s
LANGUAGES = (
    ('ru', _(u'Русский')),
#    ('en', _(u'Английский')),
)

LOCALE_PATHS = (os.path.join(PROJECT_DIR, 'locale'),)
FIXTURE_DIRS = (os.path.join(PROJECT_DIR, 'fixtures'),)

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

FRONTEND_URI = '/app/index.html'

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'collected_static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a8or7k-y_5bgkkp*%+8073l2rz_ne^j2)xj*a1m3znowuvotvw'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'utils.middleware.csrf.DisableCSRF',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'project.urls'
LOGIN_REDIRECT_URL = '/account'
LOGIN_URL = '/account/login'
LOGOUT_URL = '/account/logout'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (os.path.join(PROJECT_DIR, 'templates'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',

    'sorl.thumbnail',
    'rest_framework',
    'djcelery',
    'kombu.transport.django',
#    'south',

    'apps.account',
    'apps.picture',
    'apps.notice',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
             'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'colored': {
            '()': 'utils.log.ColoredFormatter',
            'format': '%(asctime)s %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'logs/log',
            'maxBytes': 5 * 1024 ** 2,
            'backupCount': 5
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'project': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    }
}

THUMBNAIL_PREFIX = 'userpics/cache/'

# API settings
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
}

BROKER_URL = 'django://'

try:
    from .local import *

except ImportError:
    raise ImproperlyConfigured(
        u'Please create local.py file(exapmle in deploy directory)'
    )
