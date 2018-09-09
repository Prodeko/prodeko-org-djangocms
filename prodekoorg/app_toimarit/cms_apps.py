from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from prodekoorg.app_toimarit.views import list_hallitus, list_toimarit


@apphook_pool.register
class ToimaritApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Toimarit")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', list_toimarit),
        ]


@apphook_pool.register
class HallitusApphook(CMSApp):
    app_name = "app_toimarit"
    name = _("Hallitus")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', list_hallitus),
        ]
