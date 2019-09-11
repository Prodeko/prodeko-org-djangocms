from .base import *

DEBUG = False
ALLOWED_HOSTS = ["localhost", "prodeko.org", ".prodeko.org"]

# When DEBUG = False, all errors with level ERROR or
# higher get mailed to ADMINS according to LOGGING conf
ADMINS = [("CTO", "cto@prodeko.org")]
# When DEBUG = False, all broken links get emailed to MANAGERS
MANAGERS = [("CTO", "cto@prodeko.org")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME_DEFAULT,
        "USER": DB_USER,
        "PASSWORD": DB_PSWD,
        "HOST": "localhost",
        "PORT": "3306",
    },
    "TEST": {"CHARSET": "utf8", "COLLATION": "utf8_unicode_ci"},
}

INSTALLED_APPS += ("storages",)

CDN_URL = "static.prodeko.org"

CKEDITOR_BASEPATH = f"https://{CDN_URL}/static/ckeditor/ckeditor/"

DEFAULT_FILE_STORAGE = "prodekoorg.custom_azure.AzureMediaStorage"
STATICFILES_STORAGE = "prodekoorg.custom_azure.AzureStaticStorage"

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"

STATIC_URL = f"https://{CDN_URL}/{STATIC_LOCATION}/"
MEDIA_URL = f"https://prodekostorage.blob.core.windows.net/{MEDIA_LOCATION}/"

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
