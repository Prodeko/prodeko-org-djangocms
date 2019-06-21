from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import re_path
from django.utils.translation import ugettext_lazy as _
from prodekoorg.app_toimarit.views import list_boardmembers, list_guildofficials


@apphook_pool.register
class ToimaritApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Guild officials application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [re_path(r"^", list_guildofficials)]


@apphook_pool.register
class HallitusApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Board of Prodeko application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [re_path(r"^", list_boardmembers)]
