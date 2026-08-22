from django.db import migrations

from ._drop_oauth2 import drop_oauth2_provider_tables


def forwards(apps, schema_editor):
    drop_oauth2_provider_tables(schema_editor.connection)


class Migration(migrations.Migration):
    """prodeko.org no longer issues OAuth2 tokens; the tables go with the app.

    django-oauth-toolkit is uninstalled, so django can no longer cascade the
    five tables that reference the user table, and deleting a user who once
    held a token would fail on the surviving constraint. The tables live in
    no installed app any more, which is why this drops them by hand rather
    than by reversing the library's own migrations.

    Deliberately irreversible: reinstalling the app and migrating it forward
    is what brings the tables back, not a reverse of this.
    """

    dependencies = [("auth_prodeko", "0004_unusable_passwords")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
