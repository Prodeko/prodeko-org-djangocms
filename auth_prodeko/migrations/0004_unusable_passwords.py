from django.conf import settings
from django.db import migrations

from ._retire import retire_passwords


def forwards(apps, schema_editor):
    user_model = apps.get_model("auth_prodeko", "User")
    retire_passwords(user_model, getattr(settings, "KEYCLOAK_BREAK_GLASS_EMAIL", ""))


class Migration(migrations.Migration):
    """Authentication moves to Keycloak; local passwords stop being usable.

    Deliberately irreversible: the hashes are gone once this has run, and
    restoring them is not something a reverse migration could do.
    """

    dependencies = [("auth_prodeko", "0003_keycloak_link")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
