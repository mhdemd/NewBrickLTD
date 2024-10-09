from .base import *

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_URL = "/public/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "public", "static")

MEDIA_URL = "/public/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "public", "media")


ALLOWED_HOSTS = ["newbrick.runflare.run", "www.newbrick.runflare.run"]
CSRF_TRUSTED_ORIGINS = ["https://newbrick.runflare.run"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass
