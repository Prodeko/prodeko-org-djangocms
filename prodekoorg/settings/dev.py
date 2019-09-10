from .base import *

DEBUG = True
ALLOWED_HOSTS = ["prodeko.org", ".prodeko.org", "localhost"]

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

INSTALLED_APPS += ("prodekoorg.app_vaalit",)

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
