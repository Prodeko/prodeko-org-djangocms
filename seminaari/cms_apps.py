from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import index


@apphook_pool.register
class SeminaariApphook(CMSApp):
    app_name = "seminaari"
    name = _("Prodeko seminar page")

    def get_urls(self, page=None, language=None, **kwargs):
        return [path("", index)]
