import socket

from .base import *

ROOT_URLCONF = 'config.urls.staging'


DATABASES = {
    "default": {
        "ENGINE": os.environ["SQL_ENGINE"],
        "NAME": os.environ["SQL_DATABASE"],
        "USER": os.environ["SQL_USER"],
        "PASSWORD": os.environ["SQL_PASSWORD"],
        "HOST": os.environ["SQL_HOST"],
        "PORT": os.environ["SQL_PORT"],
    }
}


CAPTCHA_TEST_MODE = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Sepimo E-commerce'
INSTALLED_APPS += [
    "admin_honeypot",
]
KAVENEGAR_API_KEY = os.environ.get('KAVENEGAR_API_KEY')

ADMINS = [(os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_EMAIL')), ]