from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from .views import posts, post, archives


@apphook_pool.register
class ProlekoApphook(CMSApp):
    app_name = "app_proleko"
    name = _("Proleko application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", posts, name="posts"),
            path(r"^posts/(?P<post_id>[0-9]+)/", post, name="post"),
            path("archives/", archives, name="archives"),
        ]
