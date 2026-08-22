from django.db import migrations


class Migration(migrations.Migration):
    """Membership applications now live in the membership registry.

    The model is deleted rather than the app uninstalled, so the foreign
    key to the user table goes with it. Leaving the constraint behind
    with no model would make deleting a user fail at the database level.

    It runs after the password retirement so that the retirement's guard,
    which aborts on an unconfigured or unusable break-glass account, is
    reached before this drops a table. A deploy that stops here otherwise
    stops with the table already gone and rolls back to an image whose
    schema no longer matches the database.
    """

    dependencies = [
        ("app_membership", "0006_pendinguser_payment_intent_id"),
        ("auth_prodeko", "0004_unusable_passwords"),
    ]

    operations = [migrations.DeleteModel(name="PendingUser")]
