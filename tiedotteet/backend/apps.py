from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TiedotteetConfig(AppConfig):
    name = "tiedotteet.backend"
    verbose_name = _("Weekly bulletin")
