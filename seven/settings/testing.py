from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seven_db',
        'USER': 'admin',
        'PASSWORD': 'PortuGal2022@',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_seven_db',
            'KEEPDB': True,  # Keep the test database to avoid recreating it
        }
    }
}

DEBUG = False