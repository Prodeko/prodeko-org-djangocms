from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppTapahtumatConfig(AppConfig):
    name = "prodekoorg.app_tapahtumat"
    verbose_name = _("Event platform")
