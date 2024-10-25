import os

from .settings import *

DEBUG = int(os.environ.get("DEBUG", default=0))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
#         'PORT': os.getenv('POSTGRES_PORT', 5432),
#         'USER': os.getenv('POSTGRES_USER', 'daboggg'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'NAME': os.getenv('POSTGRES_DB', "db01")
#     }
# }

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default=[]).split(" ")