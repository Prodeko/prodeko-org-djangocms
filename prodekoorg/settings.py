"""
Common Django settings for production and development environments.

Author: Webbitiimi
"""

import configparser
import os
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages
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
ALLOWED_HOSTS = ['new.prodeko.org', 'prodeko.org', '.prodeko.org', 'localhost']
DB_NAME_DEFAULT = config['DB']['NAME_DEFAULT']
DB_NAME_AUTH = config['DB']['NAME_AUTH']
DB_USER = config['DB']['USER']
DB_PSWD = config['DB']['PASSWORD']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME_DEFAULT,
        'USER': DB_USER,
        'PASSWORD': DB_PSWD,
        'HOST': '',
        'PORT': '',
    },
    'auth_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME_AUTH,
        'USER': DB_USER,
        'PASSWORD': DB_PSWD,
    },
    'TEST': {
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
    }
}

#DATABASE_ROUTERS = ['prodekoorg.routers.AuthRouter']

# Application definition
ROOT_URLCONF = 'prodekoorg.urls'

# Django moel used for authentication
AUTH_USER_MODEL = 'auth_prodeko.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'fi'
TIME_ZONE = 'Etc/UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Store translations here
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'prodekoorg', 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'prodekoorg', 'collected-static')


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'prodekoorg', 'static'),
    os.path.join(BASE_DIR, 'auth_prodeko', 'static'),
    os.path.join(BASE_DIR, 'prodekoorg/app_kulukorvaus', 'static'),
    os.path.join(BASE_DIR, 'prodekoorg/app_poytakirjat', 'static'),
    os.path.join(BASE_DIR, 'prodekoorg/app_tiedostot', 'static'),
    os.path.join(BASE_DIR, 'prodekoorg/app_toimarit', 'static'),
    os.path.join(BASE_DIR, 'prodekoorg/app_vaalit', 'static'),
    # tiedotteet.prodeko.org
    os.path.join(BASE_DIR, 'tiedotteet/info', 'static'),
    os.path.join(BASE_DIR, 'tiedotteet', 'public'),
    # lifelonglearning.prodeko.org
    os.path.join(BASE_DIR, 'lifelonglearning', 'static'),
]

# SASS config
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

SASS_PRECISION = 8

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'prodekoorg', 'templates'),
                 os.path.join(BASE_DIR, 'prodekoorg', 'templates', 'accounts'),
                 os.path.join(BASE_DIR, 'tiedotteet/info', 'templates'),
                 os.path.join(BASE_DIR, 'tiedotteet', 'public'),
                 os.path.join(BASE_DIR, 'lifelonglearning', 'templates'),
                 os.path.join(
                     BASE_DIR, 'prodekoorg/app_kulukorvaus', 'templates'),
                 os.path.join(
                     BASE_DIR, 'prodekoorg/app_poytakirjat', 'templates'),
                 os.path.join(BASE_DIR, 'prodekoorg/app_toimarit', 'templates')],
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

# Common templatetags across apps
OPTIONS = {
    'libraries': {
        'common_tags': os.path.join(BASE_DIR, 'prodekoorg', 'templatetags/common_tags'),
    },
}

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
    # SASS
    'sass_processor',
    # ------------------------
    # prodeko.org
    'prodekoorg',
    # ------------------------
    # Django CMS bootstrap4
    'djangocms_icon',
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',
    # ------------------------
    # tiedotteet.prodeko.org
    'tiedotteet',
    'django_wysiwyg',
    'ckeditor',
    'rest_framework',
    'corsheaders',
    # ------------------------
    # lifelonglearning.prodeko.org
    'lifelonglearning',
    # ------------------------
    'prodekoorg.app_poytakirjat',
    'prodekoorg.app_toimarit',
    'prodekoorg.app_kulukorvaus',
    'prodekoorg.app_vaalit',
    'prodekoorg.app_tiedostot',
    'prodekoorg.app_apply_for_membership',
    # ------------------------
)

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
                    ["Table", "Link", "Unlink", "Anchor", "SectionLink",
                        "Subscript", "Superscript"], ["Undo", "Redo"], ["Source"],
                    ["Maximize"]],
        'width': "auto",
        'height': "auto",
        'skin': "moono-lisa",
    },
}

"""Configure Django messages framework to work with bootstrap"""
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}
"""Email"""
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
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
