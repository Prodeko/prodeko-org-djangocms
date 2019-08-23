from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AppPoytakirjatConfig(AppConfig):
    name = "prodekoorg.app_poytakirjat"
    verbose_name = _("Board meeting documents")
