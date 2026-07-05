from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["django_extensions", "debug_toolbar", "silk"]  # noqa: F405

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", "silk.middleware.SilkyMiddleware"] + MIDDLEWARE  # noqa: F405

INTERNAL_IPS = ["127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {  # noqa: F405
    "anon": "1000/hour",
    "user": "5000/hour",
}
