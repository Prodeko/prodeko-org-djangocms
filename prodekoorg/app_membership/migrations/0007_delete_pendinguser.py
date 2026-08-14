from django.db import migrations


class Migration(migrations.Migration):
    """Membership applications now live in the membership registry.

    The model is deleted rather than the app uninstalled, so the foreign
    key to the user table goes with it. Leaving the constraint behind
    with no model would make deleting a user fail at the database level.
    """

    dependencies = [("app_membership", "0006_pendinguser_payment_intent_id")]

    operations = [migrations.DeleteModel(name="PendingUser")]
