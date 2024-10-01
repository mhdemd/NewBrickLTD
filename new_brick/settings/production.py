from .base import *

DEBUG = False

STATIC_URL = "/public/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "public", "static")

MEDIA_URL = "/public/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "public", "media")

try:
    from .local import *
except ImportError:
    pass
