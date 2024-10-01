from .base import *

DEBUG = False

STATIC_URL = "/public/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "public", "static")

MEDIA_URL = "/public/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "public", "media")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",  # تغییر به این مقدار
    },
}

ALLOWED_HOSTS = ["newbrick.runflare.run", "www.newbrick.runflare.run"]
CSRF_TRUSTED_ORIGINS = ["https://newbrick.runflare.run"]

try:
    from .local import *
except ImportError:
    pass
