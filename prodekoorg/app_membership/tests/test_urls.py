from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path

urlpatterns = i18n_patterns(
    path("", include("auth_prodeko.urls")),
    path("admin/", admin.site.urls),
    path("", include("cms.urls")),
)
