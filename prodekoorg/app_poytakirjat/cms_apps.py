from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import docs


@apphook_pool.register
class MinutesApphook(CMSApp):
    app_name = "app_poytakirjat"
    name = _("Board meeting minutes application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [path("", docs)]
