# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.static import serve

from prodekoorg.app_poytakirjat.gdrive_api import run_app_poytakirjat
from prodekoorg.app_toimarit.views import postcsv
from lifelonglearning.views import coursepage

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
    # app_toimarit & app_poytakirjat
    # Must be before admin urls
    re_path(
        r"^admin/toimarit/csvupload$",
        TemplateView.as_view(template_name="admin/uploadcsv.html"),
        name="uploadcsv",
    ),
    re_path(r"^admin/toimarit/postcsv$", postcsv, name="postcsv"),
    re_path(
        r"^admin/poytakirjat/download$",
        run_app_poytakirjat,
        name="download_docs_from_gsuite",
    ),
    # Lifelonglearning course page
    re_path(r"^lifelonglearning/course/(?P<pk>\d+)/", coursepage, name="coursepage"),
    # auth_prodeko
    re_path(r"", include("auth_prodeko.urls")),
    # app_infoscreen
    re_path(r"^infoscreen/", include("prodekoorg.app_infoscreen.urls")),
    # tiedotteet.prodeko.org
    re_path(_(r"^weekly-bulletin/"), include("tiedotteet.backend.urls")),
    # matrikkeli.prodeko.org
    re_path(_(r"^matrikkeli/"), include("alumnirekisteri.alumnirekisteri.urls")),
    # Misc
    re_path(r"^admin/", admin.site.urls),
    re_path(r"", include("cms.urls")),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = (
        [
            re_path(
                r"^media/(?P<path>.*)$",
                serve,
                {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
            )
        ]
        + staticfiles_urlpatterns()
        + urlpatterns
    )
