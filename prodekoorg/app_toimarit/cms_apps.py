from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import ugettext_lazy as _
from prodekoorg.app_toimarit.views import (
    list_current_boardmembers,
    list_old_boardmembers,
    list_current_guildofficials,
    list_old_guildofficials,
)


@apphook_pool.register
class CurrentOfficialsApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Current guild officials application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", list_current_guildofficials),
        ]


@apphook_pool.register
class OldOfficialsApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Old guild officials application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", list_old_guildofficials),
        ]


@apphook_pool.register
class CurrentBoardApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Current board of Prodeko application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", list_current_boardmembers),
        ]


@apphook_pool.register
class OldBoardsApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Old boards of Prodeko application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", list_old_boardmembers),
        ]
