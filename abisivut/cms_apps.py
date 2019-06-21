from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import re_path
from django.utils.translation import ugettext_lazy as _
from .views import index


@apphook_pool.register
class AbisivutApphook(CMSApp):
    app_name = "abit"
    name = _("High school student page")

    def get_urls(self, page=None, language=None, **kwargs):
        return [re_path(r"^", index)]
