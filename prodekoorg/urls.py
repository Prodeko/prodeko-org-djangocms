# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.static import serve
from prodekoorg.app_poytakirjat.gdrive_api import run_app_poytakirjat
from prodekoorg.app_toimarit.views import postcsv

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
]

urlpatterns += [
    url(r'^robots.txt$', TemplateView.as_view(template_name="misc/robots.txt", content_type="text/plain"), name="robots_file"),
    url(r'^browserconfig.xml$', TemplateView.as_view(template_name="misc/browserconfig.xml", content_type="text/xm l"), name="browserconfig_file"),
]

# ==== Django filer ==== #
urlpatterns += [
    url(r'^', include('filer.server.urls')),
]

# ==== tiedotteet.prodeko.org ==== #
urlpatterns += [
    url(_(r'^weekly-bulletin/'), include('tiedotteet.Tiedotteet.urls', namespace='tiedotteet')),
]

# ==== lifelonglearning.prodeko.org ==== #
urlpatterns += [
    url(r'^lifelonglearning/', include('lifelonglearning.urls', namespace='lifelonglearning')),
]

# ==== seminaari.prodeko.org ==== #
urlpatterns += [
    url(r'^seminaari/', include('seminaari.urls', namespace='seminaari')),
]

# ==== Localization and internationalization ==== #
urlpatterns += i18n_patterns(
    # ==== app_toimarit & app_poytakirjat ==== #
    # Must be before admin urls
    url(r'^admin/toimarit/csvupload$', TemplateView.as_view(template_name='admin/uploadcsv.html'), name='uploadcsv'),
    url(r'^admin/toimarit/postcsv$', postcsv, name='postcsv'),
    url(r'^admin/poytakirjat/download$', run_app_poytakirjat, name='download_docs_from_gsuite'),

    # ==== auth_prodeko ==== #
    url(r'^', include('auth_prodeko.urls', namespace='auth_prodeko')),
    # ==== app_apply_for_membership ==== #
    url(r'^', include('prodekoorg.app_apply_for_membership.urls', namespace='app_apply_for_membership')),
    # ==== app_kulukorvaus ==== #
    url(r'^', include('prodekoorg.app_kulukorvaus.urls', namespace='app_kulukorvaus')),
    # ==== app_poytakirjat ==== #
    url(r'^', include('prodekoorg.app_poytakirjat.urls', namespace='app_poytakirjat')),
    # ==== app_tiedostot ==== #
    url(r'^', include('prodekoorg.app_tiedostot.urls', namespace='app_tiedostot')),
    # ==== app_vaalit ==== #
    url(r'^', include('prodekoorg.app_vaalit.urls', namespace='app_vaalit')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ] + staticfiles_urlpatterns() + urlpatterns
