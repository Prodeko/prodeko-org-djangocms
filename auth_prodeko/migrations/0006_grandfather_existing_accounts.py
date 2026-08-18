from django.db import migrations, models

from ._grandfather import grandfather_existing_accounts


def forwards(apps, schema_editor):
    grandfather_existing_accounts(apps.get_model("auth_prodeko", "User"))


class Migration(migrations.Migration):
    """Everyone who can sign in today can still sign in tomorrow.

    Keycloak gates sign-in on a membership role, and nothing on prodeko.org
    consults membership status without it, so applying the role alone would
    shut out every former member who signs in now. Stamping the accounts that
    exist at this moment keeps them, and only them: the flag defaults to false,
    so an account created after this runs is held to the role like anyone else.
    """

    dependencies = [("auth_prodeko", "0005_drop_oauth2_provider_tables")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="predates_keycloak",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Designates whether this account existed before prodeko.org "
                    "moved to the Prodeko login. Such an account may sign in "
                    "without a current membership, which is how members who have "
                    "since left keep their access."
                ),
                verbose_name="Predates Keycloak",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
