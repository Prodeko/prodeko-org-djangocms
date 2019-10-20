from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppUtilsConfig(AppConfig):
    name = "prodekoorg.app_utils"
    verbose_name = _("Utilities")

    def ready(self):
        import prodekoorg.app_utils.signals
