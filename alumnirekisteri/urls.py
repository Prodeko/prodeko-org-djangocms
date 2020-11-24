from django.contrib import admin
from django.urls import include, path

from alumnirekisteri.rekisteri import urls as rekisteri_urls

urlpatterns = [
    path("super-admin/", include(admin.site.urls)),
    path("", include(rekisteri_urls)),
    # REST API
    # path("api-auth/", include("rest_framework.urls")),
]
