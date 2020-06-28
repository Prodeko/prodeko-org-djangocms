# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve


def get_version():
    # Increment this when javascript translations change
    version = 1
    return version


handler500 = "prodekoorg.views.handler500"

urlpatterns = [
    re_path(r"^sitemap\.xml$", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    re_path(
        r"^robots.txt$",
        TemplateView.as_view(
            template_name="misc/robots.txt", content_type="text/plain"
        ),
        name="robots_file",
    ),
    re_path(
        r"^browserconfig.xml$",
        TemplateView.as_view(
            template_name="misc/browserconfig.xml", content_type="text/xml"
        ),
        name="browserconfig_file",
    ),
]

# Django filer
urlpatterns += [re_path(r"", include("filer.server.urls"))]

# Localization and internationalization
urlpatterns += i18n_patterns(
    re_path(
        r"^jsi18n/",
        cache_page(86400, key_prefix="js18n-%s" % get_version())(
            JavaScriptCatalog.as_view()
        ),
        name="javascript-catalog",
    ),
    # auth_prodeko
    re_path(r"", include("auth_prodeko.urls")),
    # app_infoscreen
    re_path(r"^infoscreen/", include("prodekoorg.app_infoscreen.urls")),
    # tiedotteet.prodeko.org
    re_path(_(r"^weekly-bulletin/"), include("tiedotteet.backend.urls")),
    # matrikkeli.prodeko.org
    re_path(_(r"^matrikkeli/"), include("alumnirekisteri.rekisteri.urls")),
    # Misc
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    re_path(r"", include("cms.urls")),
)

# This is only needed when using runserver.
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = (
        [
            re_path(
                r"^media/(?P<path>.*)$",
                serve,
                {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
            ),
            path("__debug__/", include(debug_toolbar.urls)),
        ]
        + staticfiles_urlpatterns()
        + urlpatterns
    )
