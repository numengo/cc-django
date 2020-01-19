"""
Base settings to build other settings files upon.
"""

import environ
from decimal import Decimal
import os
from django.urls import reverse_lazy
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from cmsplugin_cascade.bootstrap4.mixins import BootstrapUtilities
from cmsplugin_cascade.extra_fields.config import PluginExtraFieldsConfig

SHOP_APP_LABEL = "{{ cookiecutter.app_name }}_shop"

PROJECT_NAME = "{{ cookiecutter.project_name }}"

APP_NAME = "{{ cookiecutter.app_name }}"

SHORT_DESCRIPTION = "{{ cookiecutter.short_description }}"

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # ({{ cookiecutter.app_name }}/config/settings/base.py - 3 = {{ cookiecutter.app_name }}/)


APPS_DIR = ROOT_DIR.path("{{ cookiecutter.app_name }}")

WORK_DIR = os.environ.get("DJANGO_WORKDIR", ROOT_DIR.path("workdir"))

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(WORK_DIR.path("fixtures")),)

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every O"S.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "{{ cookiecutter.timezone }}"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "{{ cookiecutter.languages.strip().split(",") | first }}"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
{% if cookiecutter.use_docker == "y" -%}
DATABASES = {"default": env.db("DATABASE_URL")}
{%- else %}
DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres://{% if cookiecutter.windows == 'y' %}localhost{% endif %}/{{cookiecutter.app_name}}")
}
{%- endif %}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
{%- if cookiecutter.use_celery == "y" %}
    "django_celery_beat",
{%- endif %}
    "reversion",
    "ngoutils",
]

LOCAL_APPS = [
    #### PROTECTED REGION ID({{ cookiecutter.app_name }}.settings.local_apps.gen) ENABLED START ####
        # automatically filled by code generator
    #### PROTECTED REGION END ####

    #### PROTECTED REGION ID({{ cookiecutter.app_name }}.settings.local_apps.user) ENABLED START ####
    #"{{ cookiecutter.app_name }}.users.apps.UsersConfig",
{%- if cookiecutter.use_django_shop == "y" %}
    "{{ cookiecutter.app_name }}.shop.apps.ShopConfig",
{%- endif %}
    # Your stuff: custom apps go here
    #### PROTECTED REGION END ####
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "{{ cookiecutter.app_name }}.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
#AUTH_USER_MODEL = "users.User"
AUTH_USER_MODEL = "auth.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
{%- if cookiecutter.use_django_shop == "y" %}
    "shop.middleware.CustomerMiddleware",
{%- endif %}
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(WORK_DIR.path("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    ("{{ cookiecutter.app_name }}", str(APPS_DIR.path("static"))),
    ("node_modules", str(ROOT_DIR.path("node_modules"))),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
{%- if cookiecutter.use_django_shop == "y" %}
    "sass_processor.finders.CssFinder",
{%- endif %}
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(WORK_DIR, "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "APP_DIRS": True,
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            #"loaders": [
            #    "django.template.loaders.filesystem.Loader",
            #    "django.template.loaders.app_directories.Loader"
            #],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
{%- if cookiecutter.use_django_cms == "y" %}
                "sekizai.context_processors.sekizai",
                "cms.context_processors.cms_settings",
{%- endif %}
{%- if cookiecutter.use_django_shop == "y" %}
                "shop.context_processors.customer",
                "shop.context_processors.shop_settings",
{%- endif %}
{%- if cookiecutter.use_stripe == "y" %}
                "shop_stripe.context_processors.public_keys",
{%- endif %}
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "{{ cookiecutter.app_name }}.utils.context_processors.settings_context",
            ],
        },
    },
{%- if cookiecutter.use_django_shop == "y" %}
    {
    "BACKEND": "post_office.template.backends.post_office.PostOfficeTemplates",
    "APP_DIRS": True,
    "DIRS": [],
    "OPTIONS": {
        "context_processors": [
            "django.contrib.auth.context_processors.auth",
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.static",
            "django.template.context_processors.tz",
            "django.template.context_processors.request",
            ]
        }
    },
{% endif -%}
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "SAMEORIGIN"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""{{cookiecutter.full_name}}""", "{{cookiecutter.email}}")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "post_office": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

{% if cookiecutter.use_celery == "y" -%}
# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

{%- endif %}
# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
#https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-user-models
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
#ACCOUNT_ADAPTER = "{{cookiecutter.app_name}}.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
#SOCIALACCOUNT_ADAPTER = "{{cookiecutter.app_name}}.users.adapters.SocialAccountAdapter"

SOCIALACCOUNT_PROVIDERS = {
    # https://django-allauth.readthedocs.io/en/latest/providers.html#facebook
    "facebook": {
        "METHOD": "oauth2",
        "SDK_URL": "//connect.facebook.net/{locale}/sdk.js",
        "SCOPE": ["email", "public_profile", "user_friends"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "INIT_PARAMS": {"cookie": True},
        "FIELDS": [
            "id",
            "email",
            "name",
            "first_name",
            "last_name",
            "verified",
            "locale",
            "timezone",
            "link",
            "gender",
            "updated_time",
        ],
        "EXCHANGE_TOKEN": True,
        "LOCALE_FUNC": "path.to.callable",
        "VERIFIED_EMAIL": False,
        "VERSION": "v2.12",
    }
}


{% if cookiecutter.use_compressor == "y" -%}
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
{% endif %}

{%- if cookiecutter.use_django_rest_framework == "y" %}
# DJANGO-REST
# ------------------------------------------------------------------------------
INSTALLED_APPS += [
    "rest_framework",
    "drf_yasg",
]

    {%- if cookiecutter.use_django_shop == "y" %}
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "shop.rest.money.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",  # can be disabled for production environments
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    #"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    #"PAGE_SIZE": 16,
}

REST_AUTH_SERIALIZERS = {
    "LOGIN_SERIALIZER": "shop.serializers.auth.LoginSerializer",
}
    {%- endif %}
{%- endif %}

{%- if cookiecutter.use_django_cms == "y" %}
# DJANGO-CMS
# ------------------------------------------------------------------------------
# Dummy gettext function
gettext = lambda s: s

MIDDLEWARE = ["cms.middleware.utils.ApphookReloadMiddleware"] + MIDDLEWARE + [
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware"
]

INSTALLED_APPS += [
    "cms",
    "menus",
    "sekizai",
    "treebeard",
    "djangocms_text_ckeditor",
    "filer",
    "easy_thumbnails",
    "easy_thumbnails.optimize",
    "djangocms_column",
    "djangocms_file",
    "djangocms_link",
    "djangocms_picture",
    "djangocms_style",
    "djangocms_snippet",
    "djangocms_googlemap",
    "djangocms_video",
    "categories",
    "categories.editor",

    "django_select2",
{%- if cookiecutter.use_django_shop == "y" %}
    "cmsplugin_cascade",
    "cmsplugin_cascade.clipboard",
    "cmsplugin_cascade.sharable",
    "cmsplugin_cascade.extra_fields",
    "cmsplugin_cascade.icon",
    "cmsplugin_cascade.segmentation",
    "sass_processor",
    "django_fsm",
    "fsm_admin",
    "djng",

    "rest_framework.authtoken",
    "rest_auth",
    "cms_bootstrap",
    "adminsortable2",
    #"email_auth",
    "django_filters",
    "polymorphic",
        {%- if cookiecutter.use_i18n == "y" %}
    "parler",
        {%- endif %}
    "post_office",
    "haystack",
        {%- if cookiecutter.use_paypal == "y" %}
    "shop_paypal",
        {%- endif %}
        {%- if cookiecutter.use_stripe == "y" %}
    "shop_stripe",
        {%- endif %}
        {%- if cookiecutter.use_sendcloud == "y" %}
    "shop_sendcloud",
        {%- endif %}
    "shop",
    {%- endif %}
]

# Django CMS configurations
CMS_TEMPLATES = (
    ("{{ cookiecutter.app_name }}/pages/default.html", _("Default Page")),
    ("fullwidth.html", _("Fullwidth")),
    ("sidebar_left.html", _("Sidebar Left")),
    ("sidebar_right.html", _("Sidebar Right")),
)

{%- with languages = cookiecutter.languages.replace(' ', '').split(',') %}
# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
LANGUAGES = [{% for language in languages %}
    ('{{ language }}', "{{ language }}"),{% endfor %}
]

PARLER_DEFAULT_LANGUAGE = LANGUAGE_CODE

PARLER_LANGUAGES = {
    1: [{% for language in languages %}
        {'code': '{{ language }}'},{% endfor %}
    ],
    'default': {
        'fallbacks': [{% for language in languages %}'{{ language }}'{% if not loop.last %}, {% endif %}{% endfor %}],
    },
}

CMS_LANGUAGES = {
    'default': {
        'fallbacks': [{% for language in languages %}'{{ language }}'{% if not loop.last %}, {% endif %}{% endfor %}],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
    1: [{% for language in languages %}{
        'public': True,
        'code': '{{ language }}',
        'hide_untranslated': False,
        'name': '{{ language.title() }}',
        'redirect_on_fallback': True,
    }{% if not loop.last %}, {% endif %}{% endfor %}]
}
{%- endwith %}

# settings for storing files and images

FILER_ADMIN_ICON_SIZES = ('16', '32', '48', '80', '128')

FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True

FILER_DUMP_PAYLOAD = False

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

THUMBNAIL_HIGH_RESOLUTION = False

THUMBNAIL_OPTIMIZE_COMMAND = {
    'gif': '/usr/bin/optipng {filename}',
    'jpeg': '/usr/bin/jpegoptim {filename}',
    'png': '/usr/bin/optipng {filename}'
}

THUMBNAIL_PRESERVE_EXTENSIONS = True

TEXT_SAVE_IMAGE_FUNCTION="cmsplugin_filer_image.integrations.ckeditor.create_image_plugin"
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters"
)

MIGRATION_MODULES = {
    "cmsplugin_filer_image": "cmsplugin_filer_image.migrations",
    "cmsplugin_filer_file": "cmsplugin_filer_file.migrations",
    "cmsplugin_filer_folder": "cmsplugin_filer_folder.migrations",
    "cmsplugin_filer_video": "cmsplugin_filer_video.migrations",
    "cmsplugin_filer_teaser": "cmsplugin_filer_teaser.migrations"
}


CMS_PLACEHOLDER_CONF = {
    {%- if cookiecutter.use_django_shop == "y" %}
    "Breadcrumb": {
        "plugins": ["BreadcrumbPlugin"],
        "parent_classes": {"BreadcrumbPlugin": None},
    },
    "Commodity Details": {
        "plugins": ["BootstrapContainerPlugin", "BootstrapJumbotronPlugin"],
        "parent_classes": {
            "BootstrapContainerPlugin": None,
            "BootstrapJumbotronPlugin": None,
        },
    },
    "Main Content": {
        "plugins": ["BootstrapContainerPlugin", "BootstrapJumbotronPlugin"],
        "parent_classes": {
            "BootstrapContainerPlugin": None,
            "BootstrapJumbotronPlugin": None,
            "TextLinkPlugin": ["TextPlugin", "AcceptConditionPlugin"],
        },
    },
    "Static Footer": {
        "plugins": ["BootstrapContainerPlugin", "BootstrapJumbotronPlugin"],
        "parent_classes": {
            "BootstrapContainerPlugin": None,
            "BootstrapJumbotronPlugin": None,
        },
    },
    {% endif -%}
}

    {%- if cookiecutter.use_django_shop == "y" %}
CMSPLUGIN_CASCADE_PLUGINS = [
    "cmsplugin_cascade.bootstrap4",
    "cmsplugin_cascade.segmentation",
    "cmsplugin_cascade.generic",
    "cmsplugin_cascade.icon",
    "cmsplugin_cascade.leaflet",
    "cmsplugin_cascade.link",
    "shop.cascade",
]

CMSPLUGIN_CASCADE = {
    "link_plugin_classes": [
        "shop.cascade.plugin_base.CatalogLinkPluginBase",
        #"cmsplugin_cascade.link.plugin_base.LinkElementMixin",
        "shop.cascade.plugin_base.CatalogLinkForm",
    ],
    "alien_plugins": ["TextPlugin", "TextLinkPlugin", "AcceptConditionPlugin"],
    "bootstrap4": {
        "template_basedir": "angular-ui/",
    },
    "plugins_with_extra_render_templates": {
        "CustomSnippetPlugin": [
            ("shop/catalog/product-heading.html", _("Product Heading")),
            ("{{ cookiecutter.app_name }}/catalog/manufacturer-filter.html", _("Manufacturer Filter")),
        ],
        # required to purchase real estate
        "ShopAddToCartPlugin": [
            (None, _("Default")),
            ("{{ cookiecutter.app_name }}/catalog/commodity-add2cart.html", _("Add Commodity to Cart")),
        ],
    },
    "plugins_with_sharables": {
        "BootstrapImagePlugin": ["image_shapes", "image_width_responsive", "image_width_fixed",
                                 "image_height", "resize_options"],
        "BootstrapPicturePlugin": ["image_shapes", "responsive_heights", "image_size", "resize_options"],
    },
    "plugins_with_extra_fields": {
        "BootstrapCardPlugin": PluginExtraFieldsConfig(),
        "BootstrapCardHeaderPlugin": PluginExtraFieldsConfig(),
        "BootstrapCardBodyPlugin": PluginExtraFieldsConfig(),
        "BootstrapCardFooterPlugin": PluginExtraFieldsConfig(),
        "SimpleIconPlugin": PluginExtraFieldsConfig(),
    },
    "plugins_with_extra_mixins": {
        "BootstrapContainerPlugin": BootstrapUtilities(),
        "BootstrapRowPlugin": BootstrapUtilities(BootstrapUtilities.paddings),
        "BootstrapYoutubePlugin": BootstrapUtilities(BootstrapUtilities.margins),
        "BootstrapButtonPlugin": BootstrapUtilities(BootstrapUtilities.floats),
    },
    "leaflet": {
        "tilesURL": "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}",
        "accessToken": "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw",
        "apiKey": "AIzaSyD71sHrtkZMnLqTbgRmY_NsO0A9l9BQmv4",
    },
    "bookmark_prefix": "/",
    "segmentation_mixins": [
        ("shop.cascade.segmentation.EmulateCustomerModelMixin",
         "shop.cascade.segmentation.EmulateCustomerAdminMixin"),
    ],
    "allow_plugin_hiding": True,
}

CKEDITOR_SETTINGS = {
    "language": "{% raw %}{{ language }}{% endraw %}",
    "skin": "moono-lisa",
    'toolbar_CMS': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        '/',
        ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
        ['HorizontalRule'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
        ['Source']
    ],
    "stylesSet": format_lazy("default:{}", reverse_lazy("admin:cascade_texteditor_config")),
}

CKEDITOR_SETTINGS_CAPTION = {
    "language": "{% raw %}{{ language }}{% endraw %}",
    "skin": "moono-lisa",
    "height": 70,
    "toolbar_HTMLField": [
        ["Undo", "Redo"],
        ["Format", "Styles"],
        ["Bold", "Italic", "Underline", "-", "Subscript", "Superscript", "-", "RemoveFormat"],
        ["Source"]
    ],
}

CKEDITOR_SETTINGS_DESCRIPTION = {
    "language": "{% raw %}{{ language }}{% endraw %}",
    "skin": "moono-lisa",
    "height": 250,
    "toolbar_HTMLField": [
        ["Undo", "Redo"],
        ["cmsplugins", "-", "ShowBlocks"],
        ["Format", "Styles"],
        ["TextColor", "BGColor", "-", "PasteText", "PasteFromWord"],
        ["Maximize", ""],
        "/",
        ["Bold", "Italic", "Underline", "-", "Subscript", "Superscript", "-", "RemoveFormat"],
        ["JustifyLeft", "JustifyCenter", "JustifyRight"],
        ["HorizontalRule"],
        ["NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Table"],
        ["Source"]
    ],
}

SELECT2_CSS = "node_modules/select2/dist/css/select2.min.css"
SELECT2_JS = "node_modules/select2/dist/js/select2.min.js"
SELECT2_I18N_PATH = "node_modules/select2/dist/js/i18n"

#############################################
# settings for full index text search (Haystack)

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine",
        "URL": "http://{}:9200/".format(ELASTICSEARCH_HOST),
        "INDEX_NAME": "{{ cookiecutter.app_name }}-en",
    },
        {%- if cookiecutter.use_i18n == "y" %}
    "de": {
        "ENGINE": "haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine",
        "URL": "http://{}:9200/".format(ELASTICSEARCH_HOST),
        "INDEX_NAME": "{{ cookiecutter.app_name }}-de",
    }
        {% endif -%}
}

HAYSTACK_ROUTERS = [
    "shop.search.routers.LanguageRouter",
]

############################################
# settings for django-shop and its plugins

SHOP_VALUE_ADDED_TAX = Decimal(19)
SHOP_DEFAULT_CURRENCY = "EUR"
SHOP_EDITCART_NG_MODEL_OPTIONS = "{updateOn: 'default blur', debounce: {'default': 2500, 'blur': 0}}"

SHOP_CART_MODIFIERS = [
        {%- if cookiecutter.products_model == "polymorphic" %}
    "{{ cookiecutter.app_name }}.shop.modifiers.PrimaryCartModifier",
        {%- else %}
    "shop.modifiers.defaults.DefaultCartModifier",
        {%- endif %}
    "shop.modifiers.taxes.CartExcludedTaxModifier",
        {%- if cookiecutter.products_model != "commodity" %}
    "{{ cookiecutter.app_name }}.shop.modifiers.PostalShippingModifier",
        {%- endif %}
        {%- if cookiecutter.use_paypal == "y" %}
    "shop_paypal.modifiers.PaymentModifier",
        {%- endif %}
        {%- if cookiecutter.use_stripe == "y" %}
    "{{ cookiecutter.app_name }}.shop.modifiers.StripePaymentModifier",
        {%- endif %}
    "shop.payment.modifiers.PayInAdvanceModifier",
        {%- if cookiecutter.use_sendcloud == "y" %}
    "shop_sendcloud.modifiers.SendcloudShippingModifiers",
    "shop.modifiers.defaults.WeightedCartModifier",
        {%- endif %}
    "shop.shipping.modifiers.SelfCollectionModifier",
]

SHOP_ORDER_WORKFLOWS = [
    "shop.payment.workflows.ManualPaymentWorkflowMixin",
    "shop.payment.workflows.CancelOrderWorkflowMixin",
        {%- if cookiecutter.delivery_handling == "partial" %}
    "shop.shipping.workflows.PartialDeliveryWorkflowMixin",
        {%- elif cookiecutter.delivery_handling == "common" %}
    "shop.shipping.workflows.CommissionGoodsWorkflowMixin",
        {%- else %}
    "shop.shipping.workflows.SimpleShippingWorkflowMixin",
        {%- endif %}
        {%- if cookiecutter.use_paypal == "y" %}
    "shop_paypal.payment.OrderWorkflowMixin",
        {%- endif %}
        {%- if cookiecutter.use_stripe == "y" %}
    "shop_stripe.workflows.OrderWorkflowMixin",
        {%- endif %}
]

        {% if cookiecutter.use_sendcloud == "y" -%}
SHOP_SENDCLOUD = {
    "API_KEY": os.getenv("SENDCLOUD_PUBLIC_KEY"),
    "API_SECRET": os.getenv("SENDCLOUD_SECRET_KEY"),
}
        {%- endif %}

SHOP_CASCADE_FORMS = {
    "CustomerForm": "{{ cookiecutter.app_name }}.shop.forms.CustomerForm",
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

############################################
# settings for third party Django apps
POST_OFFICE = {
    "TEMPLATE_ENGINE": "post_office",
}

NODE_MODULES_URL = STATIC_URL + "node_modules/"

SASS_PROCESSOR_INCLUDE_DIRS = [
    str(ROOT_DIR.path("node_modules")),
]

COERCE_DECIMAL_TO_STRING = True

FSM_ADMIN_FORCE_PERMIT = True

ROBOTS_META_TAGS = ("noindex", "nofollow")

SERIALIZATION_MODULES = {"json": str("shop.money.serializers")}
    {%- endif %}{# cookiecutter.use_django_shop == "y" #}

{%- endif %} {# cookiecutter.use_django_cms == "y" #}

#### PROTECTED REGION ID({{ cookiecutter.app_name }}.settings.user) ENABLED START ####
# Your stuff...
# ------------------------------------------------------------------------------
#### PROTECTED REGION END ####
