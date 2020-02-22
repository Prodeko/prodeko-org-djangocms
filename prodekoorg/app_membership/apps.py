from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppApplyForMembershipConfig(AppConfig):
    name = "prodekoorg.app_membership"
    verbose_name = _("Membership applications")

    def ready(self):
        pass
