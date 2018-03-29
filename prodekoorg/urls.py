# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.views.static import serve

from prodekoorg import views

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
    # Redirects to 'fi/main'
    url(r'^$', RedirectView.as_view(url='fi/main', permanent=False), name='index')
]

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('cms.urls'))
)

# ==== tiedotteet.prodeko.org URLS ==== #
urlpatterns += [
    url(r'^tiedotteet/', include('tiedotteet.Tiedotteet.urls', namespace='tiedotteet')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/profile', views.profile, name='profile'),
]

# Galleria
urlpatterns += [
    url(r'^gallery/', include('imagestore.urls', namespace='imagestore')),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns
