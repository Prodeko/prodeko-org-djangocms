from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from .views import posts, post, like, archives


@apphook_pool.register
class ProlekoApphook(CMSApp):
    app_name = "app_proleko"
    name = _("Proleko application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", posts, name="posts"),
            path("posts/<int:post_id>/", post, name="post"),
            path("posts/<int:post_id>/like/<int:user_id>/", like, name="like"),
            path("archives/", archives, name="archives"),
        ]
