from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-skke3wjt6mags4%jkqi1a*lwlv@3(031lq%$rydq=y(eb14-ve"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-de-01.runflare.com"
EMAIL_PORT = 465  # if use ssl
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "info@newbrickltd.co.uk"
EMAIL_HOST_PASSWORD = "newbrickltd@7477"
DEFAULT_FROM_EMAIL = "info@newbrickltd.co.uk"

try:
    from .local import *
except ImportError:
    pass
