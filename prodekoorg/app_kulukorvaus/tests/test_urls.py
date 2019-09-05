from django.conf.urls import include, url
from django.contrib import admin
from django.urls import re_path

from ..views import download_kulukorvaus_pdf, main_form

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"", include("cms.urls")),
    re_path(
        r"^download/(?P<perustiedot_id>[0-9]+)/",
        download_kulukorvaus_pdf,
        name="download_kulukorvaus",
    ),
    re_path(r"^", main_form, name="kulukorvaus"),
]
