from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppVaalitConfig(AppConfig):
    name = "prodekoorg.app_vaalit"
    verbose_name = _("Elections")
