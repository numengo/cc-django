from .base import *  # noqa
from .base import env
import six
from django.utils.translation import ugettext_lazy as _

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="!!!SET DJANGO_SECRET_KEY!!!",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

############################################
# settings for caching and storing session data
REDIS_HOST = os.getenv('REDIS_HOST')
if REDIS_HOST:
    SESSION_ENGINE = 'redis_sessions.session'

    SESSION_REDIS = {
        'host': REDIS_HOST,
        'port': 6379,
        'db': 0,
        'prefix': 'session-',
        'socket_timeout': 1
    }

    CACHES['default'] = {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://{}:6379/1'.format(REDIS_HOST),
        'OPTIONS': {
            'PICKLE_VERSION': 2 if six.PY2 else -1,
        }
    }
{% if cookiecutter.use_compressor == 'y' %}
    COMPRESS_CACHE_BACKEND = 'compressor'
    CACHES[COMPRESS_CACHE_BACKEND] = {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://{}:6379/2'.format(REDIS_HOST),
    }
{% endif %}
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 3600
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SESSION_SAVE_EVERY_REQUEST = True


# EMAIL
# ------------------------------------------------------------------------------
{% if cookiecutter.use_mailhog == 'y' and cookiecutter.use_docker == 'y' -%}
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025
{%- elif cookiecutter.use_mailhog == 'y' and cookiecutter.use_docker == 'n' -%}
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = "localhost"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025
{%- else -%}
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
{%- endif %}

# DJANGO SHOP PAYMENTS
# ------------------------------------------------------------------------------
{% if cookiecutter.use_paypal == "y" -%}
SHOP_PAYPAL = {
    "API_ENDPOINT": "https://api.sandbox.paypal.com",
    "MODE": "sandbox",
    "CLIENT_ID": os.getenv("PAYPAL_CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("PAYPAL_CLIENT_SECRET"),
    "PURCHASE_DESCRIPTION": _("Thanks for purchasing at {{ cookiecutter.project_name }}"),
}
{%- endif %}

{% if cookiecutter.use_stripe == "y" -%}
SHOP_STRIPE = {
    "PUBKEY": os.getenv("STRIPE_PUBKEY", "pk_test_HlEp5oZyPonE21svenqowhXp"),
    "APIKEY": os.getenv("STRIPE_APIKEY", "sk_test_xUdHLeFasmOUDvmke4DHGRDP"),
    "PURCHASE_DESCRIPTION": _("Thanks for purchasing at {{ cookiecutter.project_name }}"),
}

    {%- if cookiecutter.debug == "y" %}
SHOP_STRIPE_PREFILL = True
    {%- endif %}
{%- endif %}

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

META_SITE_PROTOCOL = 'http'

{% if cookiecutter.use_docker == 'y' -%}
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
{%- endif %}

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405
{% if cookiecutter.use_celery == 'y' -%}

# Celery
# ------------------------------------------------------------------------------
{% if cookiecutter.use_docker == 'n' -%}
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = True
{%- endif %}
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True

{%- endif %}
# Your stuff...
# ------------------------------------------------------------------------------
