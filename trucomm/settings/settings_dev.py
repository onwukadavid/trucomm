from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(),
        'DB_NAME': os.environ.get(),
        'DB_USER': os.environ.get(),
        'DB_HOST': os.environ.get(),
        'DB_PORT': os.environ.get(),
        'DB_PASSWORD': os.environ.get(),
    }
}