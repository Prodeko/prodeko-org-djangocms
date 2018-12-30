from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from .views import docs


@apphook_pool.register
class MinutesApphook(CMSApp):
    app_name = "app_poytakirjat"
    name = _("Minutes")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', docs)
        ]
