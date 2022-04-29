import socket

from .base import *

ROOT_URLCONF = 'config.urls.local'

INSTALLED_APPS += [
    "debug_toolbar",
]

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_email"

CAPTCHA_TEST_MODE = False