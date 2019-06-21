"""
Common Django settings for production and development environments.

Author: Webbitiimi
"""

import configparser
import os

from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Change the line below to 'prodekoorg.settings_prod' in production
from prodekoorg.settings_dev import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ID = 1
# When DEBUG = False, all errors with level ERROR or
# higher get mailed to ADMINS according to LOGGING conf
ADMINS = [("CTO", "cto@prodeko.org")]
# When DEBUG = False, all broken links get emailed to MANAGERS
MANAGERS = [("CTO", "cto@prodeko.org")]

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, "prodekoorg/variables.txt"))

# SECURITY WARNING: keep the secret keys used in production secret!
# Use configparser to read environment variables from variables.txt file
SECRET_KEY = config["DJANGO"]["SECRET"]
DEBUG = config["DEBUG"]["MODE"]
ALLOWED_HOSTS = ["new.prodeko.org", "prodeko.org", ".prodeko.org", "localhost"]
DB_NAME_DEFAULT = config["DB"]["NAME_DEFAULT"]
DB_USER = config["DB"]["USER"]
DB_PSWD = config["DB"]["PASSWORD"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME_DEFAULT,
        "USER": DB_USER,
        "PASSWORD": DB_PSWD,
        "HOST": "db",
        "PORT": "3306",
    },
    "TEST": {"CHARSET": "utf8", "COLLATION": "utf8_unicode_ci"},
}

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

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = "fi"
TIME_ZONE = "Etc/UTC"
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
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "prodekoorg/collected-static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "prodekoorg/media")

# Directories where STATICFILES_FINDERS looks for static files
# Custom apps serving static files need to be added here
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "prodekoorg/static"),
    os.path.join(BASE_DIR, "auth_prodeko/static"),
    os.path.join(BASE_DIR, "prodekoorg/app_kulukorvaus/static"),
    os.path.join(BASE_DIR, "prodekoorg/app_poytakirjat/static"),
    os.path.join(BASE_DIR, "prodekoorg/app_tiedostot/static"),
    os.path.join(BASE_DIR, "prodekoorg/app_toimarit/static"),
    os.path.join(BASE_DIR, "prodekoorg/app_vaalit/static"),
    # abit.prodeko.org
    os.path.join(BASE_DIR, "abisivut/static"),
    # lifelonglearning.prodeko.org
    os.path.join(BASE_DIR, "lifelonglearning/static"),
    # seminaari.prodeko.org
    os.path.join(BASE_DIR, "seminaari/static"),
    # tiedotteet.prodeko.org
    os.path.join(BASE_DIR, "tiedotteet/frontend/static"),
    os.path.join(BASE_DIR, "tiedotteet/frontend/public"),
    os.path.join(BASE_DIR, "tiedotteet/backend/static"),
    # matrikkeli.prodeko.org
    os.path.join(BASE_DIR, "alumnirekisteri/rekisteri/static"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]
# SASS config
# Uses: https://github.com/jrief/django-sass-processor
SASS_PRECISION = 8

# Template config
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "prodekoorg/templates"),
            os.path.join(BASE_DIR, "abisivut/templates"),
            os.path.join(BASE_DIR, "lifelonglearning/templates"),
            os.path.join(BASE_DIR, "seminaari/templates"),
            os.path.join(BASE_DIR, "tiedotteet/backend/templates"),
            os.path.join(BASE_DIR, "tiedotteet/frontend/public"),
            os.path.join(BASE_DIR, "alumnirekisteri/rekisteri"),
            os.path.join(BASE_DIR, "prodekoorg/app_apply_for_membership/templates"),
            os.path.join(
                BASE_DIR, "prodekoorg/app_apply_for_membership/templates/emails"
            ),
            os.path.join(BASE_DIR, "prodekoorg/app_kulukorvaus/templates"),
            os.path.join(BASE_DIR, "prodekoorg/app_kulukorvaus/templates/emails"),
            os.path.join(BASE_DIR, "prodekoorg/app_poytakirjat/templates"),
            os.path.join(BASE_DIR, "prodekoorg/app_toimarit/templates"),
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

# Common templatetags across different apps.
OPTIONS = {
    "libraries": {
        "common_tags": os.path.join(BASE_DIR, "prodekoorg/templatetags/common_tags")
    }
}

MIDDLEWARE = (
    "cms.middleware.utils.ApphookReloadMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
    # tiedotteet.prodeko.org
    "corsheaders.middleware.CorsMiddleware",
    # matrikkeli.prodeko.org
    #'audit_log.middleware.UserLoggingMiddleware',
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
    # auth_prodeko needs to be above 'cms'
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
    "django_wysiwyg",
    "ckeditor",
    "rest_framework",
    "corsheaders",
    # ------------------------
    # matrikkeli.prodeko.org
    "alumnirekisteri",
    "alumnirekisteri.rekisteri",
    "alumnirekisteri.auth2",
    # ------------------------
    # abit.prodeko.org
    "abisivut",
    # lifelonglearning.prodeko.org
    "lifelonglearning",
    # seminaari.prodeko.org
    "seminaari",
    # ------------------------
    "prodekoorg.app_apply_for_membership",
    "prodekoorg.app_infoscreen",
    "prodekoorg.app_kulukorvaus",
    "prodekoorg.app_poytakirjat",
    "prodekoorg.app_tiedostot",
    "prodekoorg.app_toimarit",
    # "prodekoorg.app_vaalit",
    # ------------------------
)

# DjagoCMS specific config
CMS_TEMPLATES = (
    ("abit.html", "Abit page"),
    ("contentpage/content-page.html", "Content page"),
    ("frontpage.html", "Frontpage"),
    ("seminaari.html", "Seminar page"),
    ("contentpage/content-page-twocol6-6.html", "Content page with 1:1 split"),
    ("contentpage/content-page-twocol8-4.html", "Content page with 2:1 split"),
)
CMS_PERMISSION = False
CMS_PLACEHOLDER_CONF = {}

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

# Django filer config
FILER_STORAGES = {
    "public": {
        "main": {
            "ENGINE": "filer.storage.PublicFileSystemStorage",
            "OPTIONS": {
                "location": os.path.join(BASE_DIR, "prodekoorg/media/filer"),
                "base_url": "/media/filer/",
            },
            "UPLOAD_TO": "filer.utils.generate_filename.by_date",
            "UPLOAD_TO_PREFIX": "filer_public",
        },
        "thumbnails": {
            "ENGINE": "filer.storage.PublicFileSystemStorage",
            "OPTIONS": {
                "location": os.path.join(BASE_DIR, "prodekoorg/media/filer_thumbnails"),
                "base_url": "/media/filer_thumbnails/",
            },
        },
    },
    "private": {
        "main": {
            "ENGINE": "filer.storage.PrivateFileSystemStorage",
            "OPTIONS": {
                "location": os.path.join(BASE_DIR, "prodekoorg/smedia/filer"),
                "base_url": "/smedia/filer/",
            },
            "UPLOAD_TO": "filer.utils.generate_filename.randomized",
            "UPLOAD_TO_PREFIX": "filer_public",
        },
        "thumbnails": {
            "ENGINE": "filer.storage.PrivateFileSystemStorage",
            "OPTIONS": {
                "location": os.path.join(
                    BASE_DIR, "prodekoorg/smedia/filer_thumbnails"
                ),
                "base_url": "/smedia/filer_thumbnails/",
            },
        },
    },
}

# CKEditor config.
# See https://ckeditor.com/docs/ckeditor4/latest/api/CKEDITOR_config.html
# for available options
CKEDITOR_CONFIGS = {
    "main_ckeditor": {
        "toolbar": [
            ["Format", "Bold", "Italic", "Underline", "Strike"],
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
        "width": "auto",
        "height": "auto",
        "skin": "moono-lisa",
    }
}

# Configure django messages framework to work with bootstrap
MESSAGE_TAGS = {messages.ERROR: "danger"}

# Email config. See documentation/app_apply_for_membership.md
# on more details about how email sending works through G Suite.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.gmail.com"
EMAIL_HOST_USER = config["EMAIL"]["USER"]
EMAIL_HOST_PASSWORD = config["EMAIL"]["PASSWORD"]
DEFAULT_FROM_EMAIL = "no-reply@prodeko.org"
SERVER_EMAIL = "no-reply@prodeko.org"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEV_EMAIL = config["EMAIL"]["DEV_EMAIL"]

# Loggin config. On DEBUG = FALSE, email ADMINS
# on ERROR (or higher) level events, otherwise log
# to standard output.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "mail_admins"], "level": "INFO"},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

CSRF_TRUSTED_ORIGINS = ".google.com"

# tiedotteet.prodeko.org settings
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days

CKEDITOR_BASEPATH = "/collected-static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "tiedotteet/uploads/"
DJANGO_WYSIWYG_FLAVOR = "ckeditor"
CORS_ORIGIN_ALLOW_ALL = True
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}
