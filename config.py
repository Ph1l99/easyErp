import os

ENV = os.environ.get('ENV', 'DEV')

if ENV == 'DEV':
    # DB
    DATABASE = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
    # Generic settings
    ALLOWED_HOSTS = ['*']
    DEBUG = True
    CORS_ORIGIN_ALLOW_ALL = DEBUG
    SECRET_KEY = 'django-insecure-286pkv6f3q60t6#58dv!dejud9!k#pa&yi7+pjz-(5n724s84l'
    SECRET_JWT_KEY = 'django-insecure-286pkv6f3q60t6#58dv!dejud9!k#pa&yi7+pjz-(5n724s84l'
    # Barcode settings
    ARTICLE_BARCODE_LENGTH = 24
    REPAIR_BARCODE_LENGTH = 15
    # Thermal printer settings
    THERMAL_PRINTER_VENDOR_ID = 0x04b8
    THERMAL_PRINTER_PRODUCT_ID = 0x0202
    THERMAL_PRINTER_HEADER = 'FEDE\'S ELECTRONIC\n'
    THERMAL_PRINTER_SUB_HEADER = 'di Ossola Federico\n'
    THERMAL_PRINTER_SUB_HEADER_CONTACTS = 'Contrada Tagliabo\', 16 - 21034 Cocquio-Trevisago (VA)\nTel. 03321696500\n\n'
    THERMAL_PRINTER_FOOTER_REPAIR = 'Porta con te questo scontrino per ritirare la tua riparazione!\n'

elif ENV == 'PRD':
    # DB
    DATABASE = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easyErp',
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_USER_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': 5432
    }
    # Generic settings
    ALLOWED_HOSTS = []
    DEBUG = False
    CORS_ORIGIN_ALLOW_ALL = DEBUG
    SECRET_KEY = ''
    SECRET_JWT_KEY = ''
    # Barcode settings
    ARTICLE_BARCODE_LENGTH = 24
    REPAIR_BARCODE_LENGTH = 15
    # Thermal printer settings
    THERMAL_PRINTER_VENDOR_ID = 0x04b8
    THERMAL_PRINTER_PRODUCT_ID = 0x0202
    # Printing layout
    THERMAL_PRINTER_HEADER = 'FEDE\'S ELECTRONICS\n'
    THERMAL_PRINTER_SUB_HEADER = 'di Ossola Federico\n\n'
    THERMAL_PRINTER_FOOTER_REPAIR = 'Porta con te questo scontrino per ritirare la tua riparazione!\n'
