from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppKulukorvausConfig(AppConfig):
    name = "prodekoorg.app_kulukorvaus"
    verbose_name = _("Reimbursements")
