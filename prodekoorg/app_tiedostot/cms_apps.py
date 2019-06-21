from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import re_path
from django.utils.translation import ugettext_lazy as _
from .views import main


@apphook_pool.register
class TiedostotApphook(CMSApp):
    app_name = "app_tiedostot"
    name = _("Files application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [re_path(r"^", main)]
