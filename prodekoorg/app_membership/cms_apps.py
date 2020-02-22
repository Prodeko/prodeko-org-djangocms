from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import re_path
from django.utils.translation import ugettext_lazy as _

from .views import main_form


@apphook_pool.register
class ApplyForMembershipApphook(CMSApp):
    app_name = "app_membership"
    name = _("Apply for Prodeko membership application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [re_path(r"^", main_form, name="apply")]
