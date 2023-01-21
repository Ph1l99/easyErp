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
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOWED_ORIGINS = ['http://*']
    SECRET_KEY = 'django-insecure-286pkv6f3q60t6#58dv!dejud9!k#pa&yi7+pjz-(5n724s84l'
    SECRET_JWT_KEY = 'django-insecure-286pkv6f3q60t6#58dv!dejud9!k#pa&yi7+pjz-(5n724s84l'
    # Barcode settings
    ARTICLE_BARCODE_LENGTH = 4
    REPAIR_BARCODE_LENGTH = 8
    # Thermal printer settings
    THERMAL_PRINTER_VENDOR_ID = 0x0456
    THERMAL_PRINTER_PRODUCT_ID = 0x0808
    THERMAL_PRINTER_HEADER = 'FEDE\'S ELECTRONIC\n'
    THERMAL_PRINTER_SUB_HEADER = 'di Ossola Federico\n'
    THERMAL_PRINTER_SUB_HEADER_CONTACTS = 'Contrada Tagliabo\', 16\n21034 Cocquio-Trevisago (VA)\nTel. 03321696500\n\n'
    THERMAL_PRINTER_FOOTER_REPAIR = 'Porta con te questo scontrino per ritirare la tua riparazione!\n'
    # Label printer settings
    LABEL_PRINTER_MODEL = 'QL-700'
    LABEL_PRINTER_CONNECTION_STRING = 'usb://0x04f9:0x2042'
    LABEL_PRINTER_LABEL_SIZE = '17x54'
    LABEL_PRINTER_LABEL_RESIZE_DIMENSIONS = (566, 165)
    # Inventory cycle options
    INVENTORY_CYCLE_DAYS_GAP = 6

elif ENV == 'PRD':
    # DB
    DATABASE = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': 5432
    }
    # Generic settings
    ALLOWED_HOSTS = ['easyerp.local']
    DEBUG = False
    CORS_ALLOWED_ORIGINS = ['http://*.easyerp.local', 'http://easyerp.local', 'http://easyerp.local:3000']
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_JWT_KEY = os.environ.get('SECRET_JWT_KEY')
    # Barcode settings
    ARTICLE_BARCODE_LENGTH = 24
    REPAIR_BARCODE_LENGTH = 8
    # Thermal printer settings
    THERMAL_PRINTER_VENDOR_ID = 0x0456
    THERMAL_PRINTER_PRODUCT_ID = 0x0808
    # Printing layout
    THERMAL_PRINTER_HEADER = 'FEDE\'S ELECTRONIC\n'
    THERMAL_PRINTER_SUB_HEADER = 'di Ossola Federico\n'
    THERMAL_PRINTER_SUB_HEADER_CONTACTS = 'Contrada Tagliabo\', 16\n21034 Cocquio-Trevisago (VA)\nTel. 03321696500\n\n'
    THERMAL_PRINTER_FOOTER_REPAIR = 'Porta con te questo scontrino per ritirare la tua riparazione!\n'
    # Label printer settings
    LABEL_PRINTER_MODEL = 'QL-700'
    LABEL_PRINTER_VENDOR_ID = 0x04f9
    LABEL_PRINTER_PRODUCT_ID = 0x2042
    LABEL_PRINTER_IDENTIFIER = 'usb://'
    LABEL_PRINTER_LABEL_SIZE = '17x54'
    LABEL_PRINTER_LABEL_RESIZE_DIMENSIONS = (566, 165)
    # Inventory cycle options
    INVENTORY_CYCLE_DAYS_GAP = 6
