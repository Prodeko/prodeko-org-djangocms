from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SeminaariConfig(AppConfig):
    name = "seminaari"
    verbose_name = _("Prodeko seminar")
