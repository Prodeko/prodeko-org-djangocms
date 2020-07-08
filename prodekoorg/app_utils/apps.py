from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppUtilsConfig(AppConfig):
    name = "prodekoorg.app_utils"
    verbose_name = _("Utilities")

    def ready(self):
        pass
