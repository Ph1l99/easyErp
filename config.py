import os

ENV = os.environ.get('ENV', 'DEV')

if ENV == 'DEV':
    DATABASE = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
    ALLOWED_HOSTS = ['*']
    DEBUG = True
    SECRET_KEY = 'django-insecure-286pkv6f3q60t6#58dv!dejud9!k#pa&yi7+pjz-(5n724s84l'
    SECRET_JWT_KEY = 'django-insecure-286pkv6f3q60t6#58dv!dejud9!k#pa&yi7+pjz-(5n724s84l'
    ARTICLE_BARCODE_LENGTH = 24

elif ENV == 'PRD':
    DATABASE = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easyErp',
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_USER_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': 5432
    }
    ALLOWED_HOSTS = []
    DEBUG = False
    SECRET_KEY = ''
    SECRET_JWT_KEY = ''
    ARTICLE_BARCODE_LENGTH = 24
