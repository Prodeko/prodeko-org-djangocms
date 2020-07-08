from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import download_kulukorvaus_pdf, main_form


@apphook_pool.register
class KulukorvausApphook(CMSApp):
    app_name = "app_kulukorvaus"
    name = _("Reimbursement form application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path(
                "download/<int:perustiedot_id>",
                download_kulukorvaus_pdf,
                name="download_kulukorvaus",
            ),
            path("", main_form, name="kulukorvaus"),
        ]
