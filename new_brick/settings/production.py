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


STATIC_URL = "/public/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "public", "static")

MEDIA_URL = "/public/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "public", "media")


ALLOWED_HOSTS = [
    "newbrick.runflare.run",
    "www.newbrick.runflare.run",
    "newbrickltd.co.uk",
    "www.newbrickltd.co.uk",
]

CSRF_TRUSTED_ORIGINS = ["https://newbrick.runflare.run", "https://newbrickltd.co.uk"]

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-de-01.runflare.com"
EMAIL_PORT = 465  # if use ssl
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "info@newbrickltd.co.uk"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "info@newbrickltd.co.uk"

# Caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "public", "cache"),
    }
}

MIDDLEWARE.insert(1, "django.middleware.cache.UpdateCacheMiddleware")
MIDDLEWARE.insert(3, "django.middleware.cache.FetchFromCacheMiddleware")

CACHE_MIDDLEWARE_SECONDS = 60  # 436800  # a week

try:
    from .local import *
except ImportError:
    pass
