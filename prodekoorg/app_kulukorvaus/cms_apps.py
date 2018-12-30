from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from .views import main_form


@apphook_pool.register
class KulukorvausApphook(CMSApp):
    app_name = "app_kulukorvaus"
    name = _("Reimbursement Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', main_form)
        ]
