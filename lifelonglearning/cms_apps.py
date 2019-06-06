from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import ugettext_lazy as _

from .views import coursepage, index


@apphook_pool.register
class LifelonglearningApphook(CMSApp):
    app_name = "lifelonglearning"
    name = _("Lifelonglearning page")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            re_path(r"^$", index, name="index"),
            re_path(r"^(?P<pk>\d+)/$", coursepage, name="coursepage"),
        ]
