from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import download, main


@apphook_pool.register
class TiedostotApphook(CMSApp):
    app_name = "app_tiedostot"
    name = _("Files application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", main, name="files"),
            path("/download/<pk>/", download, name="download_files"),
        ]
