from cms.appresolver import get_app_patterns
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.urls import re_path

urlpatterns = i18n_patterns(
    re_path(r"^", include("auth_prodeko.urls")), re_path(r"^", include("cms.urls"))
)

