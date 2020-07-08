from .base import *

DEBUG = True
ALLOWED_HOSTS = ["prodeko.org", ".prodeko.org", "localhost"]

INTERNAL_IPS = ["web"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME_DEFAULT,
        "USER": DB_USER,
        "PASSWORD": DB_PSWD,
        "HOST": "postgres",
        "PORT": "5432",
    }
}

# Caching
CACHES = {"default": {"BACKEND": "redis_cache.RedisCache", "LOCATION": "redis:6379"}}

if config["DEBUG"]["SHOW_DEBUG_TOOLBAR"] == "True":
    # Show django debug toolbar always.
    # This is needed because the Docker internal IP is not static
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True if DEBUG else False
    }
    INSTALLED_APPS += ("debug_toolbar",)

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

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
            "UPLOAD_TO_PREFIX": "public",
        },
        "thumbnails": {"ENGINE": "filer.storage.PublicFileSystemStorage",},
    },
    "private": {
        "main": {
            "ENGINE": "filer.storage.PrivateFileSystemStorage",
            "OPTIONS": {
                "location": os.path.join(BASE_DIR, "prodekoorg/smedia/filer"),
                "base_url": "/smedia/filer/",
            },
            "UPLOAD_TO": "filer.utils.generate_filename.randomized",
            "UPLOAD_TO_PREFIX": "private",
        },
        "thumbnails": {"ENGINE": "filer.storage.PrivateFileSystemStorage",},
    },
}
