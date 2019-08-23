from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthProdekoConfig(AppConfig):
    name = "auth_prodeko"
    verbose_name = _("Prodeko authentication")

    def ready(self):
        import auth_prodeko.signals
