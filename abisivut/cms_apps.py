from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from .views import index


@apphook_pool.register
class AbisivutApphook(CMSApp):
    app_name = "abit"
    name = _("High school student page")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', index),
        ]
