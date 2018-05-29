"""
Common Django settings for production and development environments.

Author: Webbitiimi
"""

import configparser
import os
from django.utils.translation import gettext_lazy as _
# Change the line below to 'prodekoorg.settings_prod' in production
from prodekoorg.settings_dev import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ID = 1

LOGIN_URL = '/login/'

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'prodekoorg/variables.txt'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['DJANGO']['SECRET']
DEBUG = config['DEBUG']['MODE']
ALLOWED_HOSTS = ['djangocms.prodeko.org', 'prodeko.org', '.prodeko.org', 'localhost']
DB_NAME = config['DB']['NAME']
DB_USER = config['DB']['USER']
DB_PSWD = config['DB']['PASSWORD']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PSWD,
        'HOST': '',
        'PORT': '',
    }
}

# Application definition
ROOT_URLCONF = 'prodekoorg.urls'

# Django moel used for authentication
AUTH_USER_MODEL = 'auth_prodeko.User'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Etc/UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'prodekoorg', 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'prodekoorg', 'collected-static')


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'prodekoorg', 'static'),
    # tiedotteet.prodeko.org
    os.path.join(BASE_DIR, 'tiedotteet/info', 'static'),
    os.path.join(BASE_DIR, 'tiedotteet', 'public'),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'prodekoorg', 'templates'),
                 os.path.join(BASE_DIR, 'tiedotteet/info', 'templates'),
                 os.path.join(BASE_DIR, 'tiedotteet', 'public'),
                 os.path.join(BASE_DIR, 'prodekoorg/app_toimarit', 'templates'),
                 os.path.join(BASE_DIR, 'prodekoorg/app_kulukorvaus', 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        },
    },
]


MIDDLEWARE = (
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    # tiedotteet.prodeko.org
    'corsheaders.middleware.CorsMiddleware',
)

INSTALLED_APPS = (
    # Django defaults
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    # ------------------------
    # auth_prodeko needs to be above 'cms'
    'auth_prodeko',
    # ------------------------
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    # Django CMS plugins
    'djangocms_column',
    'djangocms_file',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_video',
    'prodekoorg',
    # ------------------------
    # tiedotteet.prodeko.org
    'tiedotteet',
    'django_wysiwyg',
    'ckeditor',
    'rest_framework',
    'corsheaders',
    # ------------------------
    'prodekoorg.app_poytakirjat',
    'prodekoorg.app_toimarit',
    'prodekoorg.app_kulukorvaus',
    'prodekoorg.app_vaalit',
    'prodekoorg.app_tiedostot',
)

"""Language settings"""
LANGUAGES = (
    ('fi', _('Finnish')),
    ('en', _('English')),
)

LANGUAGE_FALLBACK = None

CMS_LANGUAGES = {
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'fi',
            'hide_untranslated': False,
            'name': _('Finnish'),
            'redirect_on_fallback': True,
        },
        {
            'public': True,
            'code': 'en',
            'hide_untranslated': False,
            'name': _('English'),
            'redirect_on_fallback': True,
        },
    ],
}

"""CMS template registration"""
CMS_TEMPLATES = (
    ('contentpage/content-page.html', 'Content page'),
    ('frontpage.html', 'Frontpage'),
    ('contentpage/content-page-twocol6-6.html', 'Content page with 1:1 split'),
    ('contentpage/content-page-twocol8-4.html', 'Content page with 2:1 split'),
)
CMS_PERMISSION = True
CMS_PLACEHOLDER_CONF = {}
MIGRATION_MODULES = {}
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

"""Django filer settings"""
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(BASE_DIR, 'prodekoorg/media/filer'),
                'base_url': '/media/filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(BASE_DIR, 'prodekoorg/media/filer_thumbnails'),
                'base_url': '/media/filer_thumbnails/',
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(BASE_DIR, 'prodekoorg/smedia/filer'),
                'base_url': '/smedia/filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(BASE_DIR, 'prodekoorg/smedia/filer_thumbnails'),
                'base_url': '/smedia/filer_thumbnails/',
            },
        },
    },
}

"""CKEditor"""
CKEDITOR_CONFIGS = {
    'vaalit_ckeditor': {
        'toolbar': [["Format", "Bold", "Italic", "Underline", "Strike"],
                    ["NumberedList", 'BulletedList', "Indent", "Outdent", "JustifyLeft", "JustifyCenter",
                    "JustifyRight", "JustifyBlock"],
                    ["Table", "Link", "Unlink", "Anchor", "SectionLink", "Subscript", "Superscript"], ["Undo", "Redo"], ["Source"],
                    ["Maximize"]],
        'width': "auto",
        'height': "auto"
    },
}
"""Email"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = True

"""tiedotteet.prodeko.org settings"""
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days

CKEDITOR_UPLOAD_PATH = "tiedotteet/uploads/"
DJANGO_WYSIWYG_FLAVOR = "ckeditor"
CORS_ORIGIN_ALLOW_ALL = True
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
