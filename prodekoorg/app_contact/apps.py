from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppContactConfig(AppConfig):
    name = "prodekoorg.app_contact"
    verbose_name = _("Contact form")
