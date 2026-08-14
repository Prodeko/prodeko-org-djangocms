from django.apps import AppConfig


class AppMembershipConfig(AppConfig):
    """Retained only to keep this app's migration history applicable.

    Membership applications are handled by membership.prodeko.org.
    """

    name = "prodekoorg.app_membership"
    verbose_name = "Membership (retired)"
