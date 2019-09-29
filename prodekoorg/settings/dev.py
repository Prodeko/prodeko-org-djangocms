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
        "OPTIONS": {"charset": "utf8mb4"},
    },
    "TEST": {"CHARSET": "utf8", "COLLATION": "utf8_unicode_ci"},
}

INSTALLED_APPS += ("prodekoorg.app_vaalit",)

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
            "UPLOAD_TO_PREFIX": "files/public",
        },
        "thumbnails": {
            "ENGINE": "filer.storage.PublicFileSystemStorage",
            "OPTIONS": {
                "location": os.path.join(BASE_DIR, "prodekoorg/media/filer/filer_thumbnails"),
                "base_url": MEDIA_URL + "thumbnails",
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
            "UPLOAD_TO_PREFIX": "files/private",
        },
        "thumbnails": {
            "ENGINE": "filer.storage.PrivateFileSystemStorage",
            "OPTIONS": {
                "location": os.path.join(
                    BASE_DIR, "prodekoorg/smedia/filer/filer_thumbnails"
                ),
                "base_url": MEDIA_URL + "thumbnails",
            },
        },
    },
}
