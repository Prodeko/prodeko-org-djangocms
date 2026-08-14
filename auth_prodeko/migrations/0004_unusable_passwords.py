from django.conf import settings
from django.db import migrations

from ._retire import retire_passwords


class NoBreakGlassAccount(RuntimeError):
    """Raised when KEYCLOAK_BREAK_GLASS_EMAIL is not configured."""


def forwards(apps, schema_editor):
    break_glass_email = getattr(settings, "KEYCLOAK_BREAK_GLASS_EMAIL", "")
    if not break_glass_email:
        raise NoBreakGlassAccount(
            "KEYCLOAK_BREAK_GLASS_EMAIL is empty, so this migration would "
            "retire every password including the break-glass account's. Set "
            "[KEYCLOAK] BREAK_GLASS_EMAIL in the settings variables file and "
            "run migrate again."
        )
    user_model = apps.get_model("auth_prodeko", "User")
    retire_passwords(user_model, break_glass_email)


class Migration(migrations.Migration):
    """Authentication moves to Keycloak; local passwords stop being usable.

    Deliberately irreversible: the hashes are gone once this has run, and
    restoring them is not something a reverse migration could do. It therefore
    refuses to run at all unless a break-glass account is configured, so an
    outage of the identity provider cannot lock us out of our own site.
    """

    dependencies = [("auth_prodeko", "0003_keycloak_link")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
