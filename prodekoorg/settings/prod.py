from .base import *

DEBUG = False
# 127.0.0.1 is the deploy health check: deploy.sh curls gunicorn on loopback.
ALLOWED_HOSTS = [
    "prodeko.org",
    ".prodeko.org",
    "prodeko.fi",
    ".prodeko.fi",
    "0.0.0.0",
    "127.0.0.1",
]

# Caddy terminates TLS and reverse-proxies plain http to gunicorn on
# 127.0.0.1:8000, so request.is_secure() is False and every absolute URL Django
# builds starts with http://. mozilla_django_oidc derives the OIDC redirect_uri
# and the post_logout_redirect_uri from request.build_absolute_uri(), and
# Keycloak matches those against its registered https:// URIs, so without this
# every login fails with "Invalid parameter: redirect_uri". Only sound here:
# the header is client-supplied, and Caddy is what overwrites it.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ALLOWED_ORIGINS = ["https://ilmo.prodeko.org", "https://browser.sentry-cdn.com"]

# When DEBUG = False, all errors with level ERROR or
# higher get mailed to ADMINS according to LOGGING conf
ADMINS = [("CTO", "cto@prodeko.org")]
# When DEBUG = False, all broken links get emailed to MANAGERS
MANAGERS = [("CTO", "cto@prodeko.org")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME_DEFAULT,
        "USER": DB_USER,
        "PASSWORD": DB_PSWD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "CONN_MAX_AGE": None,
        "DISABLE_SERVER_SIDE_CURSORS": True,
    }
}

INSTALLED_APPS += ("storages",)

CDN_URL = "static.prodeko.org"
AZURE_CUSTOM_DOMAIN = CDN_URL
AZURE_CACHE_CONTROL = "public,max-age=31536000,immutable"

STORAGES = {
    "thumbnail": {
        "BACKEND": "easy_thumbnails.storage.ThumbnailFileSystemStorage",
    },
    "default": {
        "BACKEND": "prodekoorg.custom_azure.AzureMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "prodekoorg.custom_azure.AzureStaticStorage",
    },
}

# THUMBNAIL_DEFAULT_STORAGE = "prodekoorg.custom_azure.AzureMediaStorage"

# Query database for existing thumbnail aliases instead of querying remote storage.
# THUMBNAIL_CACHE_DIMENSIONS = True

# If DB cache is not found, query the remote storage first instead of generating it.
# THUMBNAIL_CHECK_CACHE_MISS = True

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"

STATIC_URL = f"https://{CDN_URL}/{STATIC_LOCATION}/"
MEDIA_URL = f"https://{CDN_URL}/{MEDIA_LOCATION}/"

# For django-ckeditor
CKEDITOR_BASEPATH = f"https://{CDN_URL}/static/ckeditor/ckeditor/"
# For djangocms-text-ckeditor
TEXT_CKEDITOR_BASE_PATH = f"https://{CDN_URL}/static/djangocms_text_ckeditor/ckeditor/"

# Django filer config
FILER_STORAGES = {
    "public": {
        "main": {
            "ENGINE": "prodekoorg.custom_azure.AzureMediaStorage",
            "UPLOAD_TO": "filer.utils.generate_filename.by_date",
            "UPLOAD_TO_PREFIX": "public",
        },
        "thumbnails": {"ENGINE": "prodekoorg.custom_azure.AzureMediaStorage"},
    },
    "private": {
        "main": {
            "ENGINE": "prodekoorg.custom_azure.AzureMediaStorage",
            "UPLOAD_TO": "filer.utils.generate_filename.randomized",
            "UPLOAD_TO_PREFIX": "private",
        },
        "thumbnails": {"ENGINE": "prodekoorg.custom_azure.AzureMediaStorage"},
    },
}

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
        # The sign-in path, ours and the library's. Only the loggers named
        # here have a handler, and every account question a member raises
        # -- refused, adopted by the wrong row, created twice -- is
        # answered by these lines and by nothing else in the container.
        "auth_prodeko": {"handlers": ["console", "mail_admins"], "level": "INFO"},
        "mozilla_django_oidc": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
    },
}
