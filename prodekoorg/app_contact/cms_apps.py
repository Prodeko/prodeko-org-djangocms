from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import main_form


@apphook_pool.register
class ContactApphook(CMSApp):
    app_name = "app_contact"
    name = _("Contact form application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [path("", main_form, name="contact")]
