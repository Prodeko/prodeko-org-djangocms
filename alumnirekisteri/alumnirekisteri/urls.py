from django.urls import include, re_path

from alumnirekisteri.rekisteri import urls as rekisteri_urls

urlpatterns = [
    re_path(r"^", include(rekisteri_urls)),
    # REST API
    re_path(r"^api-auth/", include("rest_framework.urls")),
]
