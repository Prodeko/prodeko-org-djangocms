from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import main_form, done
from .views_api import create_payment, payment_webhook


@apphook_pool.register
class ApplyForMembershipApphook(CMSApp):
    app_name = "app_membership"
    name = _("Apply for Prodeko membership application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [path("", main_form, name="apply"), path("done/", done, name="done"), path("create-payment-intent/", create_payment, name="checkout"), path("payment-webhook/", payment_webhook, name="webhook")]
