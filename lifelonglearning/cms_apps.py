from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from .views import coursepage, index


@apphook_pool.register
class LifelonglearningApphook(CMSApp):
    app_name = "lifelonglearning"
    name = _("Lifelong learning page")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", index, name="index"),
            path("course/<pk>/", coursepage, name="coursepage"),
        ]
