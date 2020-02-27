from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from .views import index, stream


@apphook_pool.register
class KiltiskameraApphook(CMSApp):
    app_name = "app_kiltiskamera"
    name = _("Guild room camera application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", index),
            path("stream", stream, name="stream"),
        ]
