from .base import *

DEBUG = False

INSTALLED_APPS.extend([

])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ["0.0.0.0", "192.168.1.134"]