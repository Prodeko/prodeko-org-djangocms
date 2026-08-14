"""
Common Django settings for production and development environments.

Author: Webbitiimi
"""

import configparser
import os

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SITE_ID = 1

# interpolation=None: values are opaque secrets, and a literal % in one
# would otherwise raise InterpolationSyntaxError at import time.
config = configparser.ConfigParser(interpolation=None)
config.read(os.path.join(BASE_DIR, "prodekoorg/settings/variables.txt"))

# SECURITY WARNING: keep the secret keys used in production secret!
# Use configparser to read environment variables from variables.txt file
SECRET_KEY = config["DJANGO"]["SECRET"]
DB_HOST = config["DB"]["HOST"]
DB_PORT = config["DB"]["PORT"]
DB_NAME_DEFAULT = config["DB"]["NAME_DEFAULT"]
DB_USER = config["DB"]["USER"]
DB_PSWD = config["DB"]["PASSWORD"]
DEV_EMAIL = config["EMAIL"]["DEV_EMAIL"]
STORAGE_KEY = config["STORAGE"]["KEY"]
SENTRY_DSN = config["SENTRY"]["DSN"]
SENTRY_ENV = config["SENTRY"]["ENV"]
MAILCHIMP_API_KEY = config["MAILCHIMP"]["MAILCHIMP_API_KEY"]
MAILCHIMP_LIST_ID = config["MAILCHIMP"]["MAILCHIMP_LIST_ID"]
STRIPE_API_KEY = config["STRIPE"]["STRIPE_API_KEY"]
STRIPE_PAYMENT_LINK_ID = config["STRIPE"]["STRIPE_PAYMENT_LINK_ID"]
STRIPE_ENDPOINT_SECRET = config["STRIPE"]["STRIPE_ENDPOINT_SECRET"]
STRIPE_APPLICATION_ENDPOINT_SECRET = config["STRIPE"][
    "STRIPE_APPLICATION_ENDPOINT_SECRET"
]

# Keycloak SSO. The section is optional so that deploy.sh's collectstatic
# and migrate steps still start on a host where Ansible has not yet
# rendered it.
KEYCLOAK_ISSUER = config.get("KEYCLOAK", "ISSUER", fallback="")
KEYCLOAK_CLIENT_ID = config.get("KEYCLOAK", "CLIENT_ID", fallback="")
KEYCLOAK_CLIENT_SECRET = config.get("KEYCLOAK", "CLIENT_SECRET", fallback="")
KEYCLOAK_BREAK_GLASS_EMAIL = config.get("KEYCLOAK", "BREAK_GLASS_EMAIL", fallback="")

# Realm roles. Membership grants access to the site at all; the other two
# grant Django's is_staff and is_superuser. All three are overwritten on
# every login, so Keycloak is the only place they are managed.
KEYCLOAK_MEMBERSHIP_ROLES = ["membership"]
KEYCLOAK_STAFF_ROLE = "prodeko-org-admin"
KEYCLOAK_SUPERUSER_ROLE = "prodeko-org-superuser"

# Application definition
ROOT_URLCONF = "prodekoorg.urls"

# Model used for authentication
AUTH_USER_MODEL = "auth_prodeko.User"
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "auth_prodeko:login"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 9},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://prodeko_org_redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = "fi"
TIME_ZONE = "Europe/Helsinki"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Translations are stored in locale/ folder
# See README to learn how to use translations
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

# Language settings
LANGUAGES = (("fi", _("Finnish")), ("en", _("English")))

LANGUAGE_FALLBACK = None

CMS_LANGUAGES = {
    1: [
        {
            "public": True,
            "code": "fi",
            "hide_untranslated": True,
            "name": _("Finnish"),
            "redirect_on_fallback": False,
        },
        {
            "public": True,
            "code": "en",
            "hide_untranslated": True,
            "name": _("English"),
            "redirect_on_fallback": False,
        },
    ],
    "default": {
        "public": True,
        "fallbacks": ["fi"],
        "hide_untranslated": False,
        "redirect_on_fallback": False,
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "prodekoorg/collected-static")
MEDIA_ROOT = os.path.join(BASE_DIR, "prodekoorg/media")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "tiedotteet/frontend/src/static"),
    os.path.join(BASE_DIR, "tiedotteet/frontend/public"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

# SASS config
# Uses: https://github.com/jrief/django-sass-processor
SASS_PRECISION = 8
# The production image bakes CSS at build time under non-prod settings, so
# output style must not depend on DEBUG.
SASS_OUTPUT_STYLE = "compressed"

# Template config
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "tiedotteet/frontend/public"),
            os.path.join(BASE_DIR, "prodekoorg/app_membership/templates/emails"),
            os.path.join(BASE_DIR, "prodekoorg/app_contact/templates/emails"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "sekizai.context_processors.sekizai",
                "django.template.context_processors.static",
                "cms.context_processors.cms_settings",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]

MIDDLEWARE = (
    "django.middleware.cache.UpdateCacheMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "cms.middleware.utils.ApphookReloadMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
    # matrikkeli.prodeko.org
    # "audit_log.middleware.UserLoggingMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
)

INSTALLED_APPS = (
    # Django defaults
    "djangocms_admin_style",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    # ------------------------
    # auth_prodeko needs to be above "cms"
    "auth_prodeko",
    # ------------------------
    "cms",
    "menus",
    "sekizai",
    "treebeard",
    "djangocms_text_ckeditor",
    "filer",
    "easy_thumbnails",
    # Django CMS plugins
    "djangocms_column",
    "djangocms_file",
    "djangocms_link",
    "djangocms_picture",
    "djangocms_style",
    "djangocms_snippet",
    "djangocms_video",
    # SASS
    "sass_processor",
    # ------------------------
    # prodeko.org
    "prodekoorg",
    # ------------------------
    # Django CMS bootstrap4
    "djangocms_icon",
    "djangocms_bootstrap4",
    "djangocms_bootstrap4.contrib.bootstrap4_alerts",
    "djangocms_bootstrap4.contrib.bootstrap4_badge",
    "djangocms_bootstrap4.contrib.bootstrap4_card",
    "djangocms_bootstrap4.contrib.bootstrap4_carousel",
    "djangocms_bootstrap4.contrib.bootstrap4_collapse",
    "djangocms_bootstrap4.contrib.bootstrap4_content",
    "djangocms_bootstrap4.contrib.bootstrap4_grid",
    "djangocms_bootstrap4.contrib.bootstrap4_jumbotron",
    "djangocms_bootstrap4.contrib.bootstrap4_link",
    "djangocms_bootstrap4.contrib.bootstrap4_listgroup",
    "djangocms_bootstrap4.contrib.bootstrap4_media",
    "djangocms_bootstrap4.contrib.bootstrap4_picture",
    "djangocms_bootstrap4.contrib.bootstrap4_tabs",
    "djangocms_bootstrap4.contrib.bootstrap4_utilities",
    # ------------------------
    # tiedotteet.prodeko.org
    "tiedotteet.backend",
    "ckeditor",
    "ckeditor_uploader",
    "rest_framework",
    "corsheaders",
    # ------------------------
    # matrikkeli.prodeko.org
    "alumnirekisteri.rekisteri",
    # ------------------------
    # abit.prodeko.org
    "abisivut",
    # lifelonglearning.prodeko.org
    "lifelonglearning",
    # seminaari.prodeko.org
    "seminaari",
    # ------------------------
    "prodekoorg.app_contact",
    "prodekoorg.app_kiltiskamera",
    "prodekoorg.app_infoscreen",
    "prodekoorg.app_membership",
    "prodekoorg.app_poytakirjat",
    "prodekoorg.app_proleko",
    "prodekoorg.app_tiedostot",
    "prodekoorg.app_toimarit",
    "prodekoorg.app_utils",
    "prodekoorg.app_vaalit",
    # ------------------------
)

# DjagoCMS specific config
CMS_TEMPLATES = (
    ("frontpage.html", _("Frontpage")),
    ("contentpage/content-page.html", _("Content page")),
    ("contentpage/content-page-twocol6-6.html", _("Content page with 1:1 split")),
    ("contentpage/content-page-twocol8-4.html", _("Content page with 2:1 split")),
    ("abit.html", _("High school student page")),
    ("lifelonglearning.html", _("Lifelong learning page")),
)
CMS_PERMISSION = True
CMS_PLACEHOLDER_CONF = {
    "abit_nav": {"name": _("Navigation"), "plugins": ["TextPlugin"]}
}
CMS_CACHE_DURATIONS = {
    "content": 60 * 60 * 6,
    "menus": 60 * 60 * 6,
    "permissions": 60 * 60 * 6,
}
CMS_PLACEHOLDER_CACHE = True
CMS_PAGE_CACHE = True

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

THUMBNAIL_ALIASES = {
    "": {
        "avatar": {"size": (50, 50), "crop": True},
        "toimari": {"size": (350, 350), "crop": True},
        "hallitus": {"size": (400, 400), "crop": True},
        "ehdokas": {"size": (150, 150), "crop": True},
    }
}

THUMBNAIL_BASEDIR = "image_thumbnails"
THUMBNAIL_HIGH_RESOLUTION = True

STORAGES = {
    "thumbnail": {
        "BACKEND": "easy_thumbnails.storage.ThumbnailFileSystemStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Config for djangocms-text-ckeditor
CKEDITOR_SETTINGS = {
    "language": "en",
    "toolbar_HTMLField": [
        ["Format", "TextColor", "BGColor", "Bold", "Italic", "Underline", "Strike"],
        [
            "NumberedList",
            "BulletedList",
            "Indent",
            "Outdent",
            "JustifyLeft",
            "JustifyCenter",
            "JustifyRight",
            "JustifyBlock",
        ],
        [
            "Table",
            "Link",
            "Unlink",
            "Anchor",
            "SectionLink",
            "Subscript",
            "Superscript",
        ],
        ["Undo", "Redo"],
        ["Source"],
        ["Maximize"],
    ],
    "skin": "moono-lisa",
}

# Config for django-ckeditor
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "width": "100%",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
            ["Styles", "Format", "Font", "FontSize"],
            ["TextColor", "BGColor"],
            ["Image"],
        ],
    }
}

# Filer global options
FILER_PAGINATE_BY = 50

# Configure django messages framework to work with bootstrap
MESSAGE_TAGS = {messages.ERROR: "danger"}

# Email config. See documentation/app_membership.md
# on more details about how email sending works through G Suite.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config["EMAIL"]["HOST"]
EMAIL_HOST_USER = config["EMAIL"]["USER"]
EMAIL_HOST_PASSWORD = config["EMAIL"]["PASSWORD"]
DEFAULT_FROM_EMAIL = "no-reply@prodeko.org"
SERVER_EMAIL = "no-reply@prodeko.org"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Error reports are mailed synchronously inside the request cycle
# (AdminEmailHandler); without a timeout a slow SMTP server can hang
# every gunicorn worker thread.
EMAIL_TIMEOUT = 10

CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

CSRF_TRUSTED_ORIGINS = [
    "https://prodeko.org",
    "https://www.prodeko.org",
    "https://prodeko.fi",
    "https://www.prodeko.fi",
    "https://*.google.com",
]

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

AUTHENTICATION_BACKENDS = (
    "auth_prodeko.oidc.backend.KeycloakOIDCBackend",
    # Kept for the single break-glass account, so an outage of the
    # identity provider cannot lock us out of our own site.
    "django.contrib.auth.backends.ModelBackend",
)

_OIDC = f"{KEYCLOAK_ISSUER}/protocol/openid-connect"
OIDC_RP_CLIENT_ID = KEYCLOAK_CLIENT_ID
OIDC_RP_CLIENT_SECRET = KEYCLOAK_CLIENT_SECRET
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = "openid email profile"
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{_OIDC}/auth"
OIDC_OP_TOKEN_ENDPOINT = f"{_OIDC}/token"
OIDC_OP_USER_ENDPOINT = f"{_OIDC}/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"{_OIDC}/certs"
OIDC_OP_LOGOUT_ENDPOINT = f"{_OIDC}/logout"
OIDC_USE_PKCE = True
OIDC_PKCE_CODE_CHALLENGE_METHOD = "S256"
OIDC_CREATE_USER = True
OIDC_STORE_ID_TOKEN = True
LOGOUT_REDIRECT_URL = "/"
OIDC_OP_LOGOUT_URL_METHOD = "auth_prodeko.oidc.logout.provider_logout"
# Where a login Keycloak allowed but this site refused ends up. The
# library redirects to this value without resolving a view name, so it
# has to be a path; reverse_lazy defers building it until the URLconf
# is loaded, and picks up the language prefix of i18n_patterns.
LOGIN_REDIRECT_URL_FAILURE = reverse_lazy("auth_prodeko:login_failed")

# Django sessions last 30 days; a Keycloak session does not. Without this
# recheck, a role revoked in Keycloak would keep working for weeks.
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 60 * 15
OIDC_EXEMPT_URLS = [
    "oidc_authentication_init",
    "oidc_authentication_callback",
    "oidc_logout",
]
# A recheck Keycloak answers but the backend refuses has to end the
# Django session, or the recheck runs again on the next request.
OIDC_CALLBACK_CLASS = "auth_prodeko.oidc.callback.KeycloakOIDCCallbackView"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    )
}

META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = "https://prodeko.org"
META_SITE_NAME = "Tuotantotalouden kilta Prodeko ry"
META_USE_OG_PROPERTIES = True
META_FB_AUTHOR_URL = "https://www.facebook.com/prodeko"
META_FB_PUBLISHER = "https://www.facebook.com/prodeko"

FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True
