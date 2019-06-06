from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import re_path
from django.utils.translation import ugettext_lazy as _
from .views import docs


@apphook_pool.register
class MinutesApphook(CMSApp):
    app_name = "app_poytakirjat"
    name = _("Board meeting minutes application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [re_path(r"^$", docs)]
