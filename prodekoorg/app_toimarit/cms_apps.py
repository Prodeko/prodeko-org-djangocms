from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from prodekoorg.app_toimarit.views import list_boardmembers, list_guildofficials


@apphook_pool.register
class ToimaritApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Guild officials application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', list_guildofficials),
        ]


@apphook_pool.register
class HallitusApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Board of Prodeko application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', list_boardmembers),
        ]
