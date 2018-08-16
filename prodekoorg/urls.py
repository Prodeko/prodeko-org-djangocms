# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView, TemplateView
from django.views.static import serve
from prodekoorg import views
from prodekoorg.app_poytakirjat.gdrive_api import run_app_poytakirjat
from prodekoorg.app_toimarit.views import *

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
    # Redirects to 'fi/main'
    #url(r'^$', RedirectView.as_view(url='fi/main', permanent=False), name='index')
]

# ==== app_toimarit ==== #
urlpatterns += [
    # Must be before admin urls
    url(r'^admin/toimarit/csvupload$', TemplateView.as_view(template_name='admin/uploadcsv.html'), name='uploadcsv'),
    url(r'^admin/toimarit/postcsv$', postcsv, name='postcsv'),
    url(r'^admin/poytakirjat/download$', run_app_poytakirjat, name='download_docs_from_gsuite'),
]

# ==== Localization and internationalization ==== #
urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls'))
)

# ==== Django filer ==== #
urlpatterns += [
    url(r'^', include('filer.server.urls')),
]

# ==== tiedotteet.prodeko.org ==== #
urlpatterns += [
    url(r'^tiedotteet/', include('tiedotteet.Tiedotteet.urls', namespace='tiedotteet')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/profile', views.profile, name='profile'),
]

# ==== app_poytakirjat ==== #
urlpatterns += [
    url(r'^', include('prodekoorg.app_poytakirjat.urls', namespace='app_poytakirjat')),
]

# ==== app_kulukorvaus ==== #
urlpatterns += [
    url(r'^', include('prodekoorg.app_kulukorvaus.urls', namespace='app_kulukorvaus')),
]

# ==== app_vaalit ==== #
urlpatterns += [
    url(r'^', include('prodekoorg.app_vaalit.urls', namespace='app_vaalit')),
]

# ==== app_tiedostot ==== #
urlpatterns += [
    url(r'^', include('prodekoorg.app_tiedostot.urls', namespace='app_tiedostot')),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ] + staticfiles_urlpatterns() + urlpatterns
