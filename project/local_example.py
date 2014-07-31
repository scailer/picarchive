DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'project/picarchive.db',
    }
}

EMAIL_HOST = ''
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'no-reply@myhost.ru'
EMAIL_SUBJECT_PREFIX = '[PicArchive] '
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False
