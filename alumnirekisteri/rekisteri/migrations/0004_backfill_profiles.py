from django.conf import settings
from django.db import migrations

from ._backfill import backfill_profiles


def forwards(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    user_model = apps.get_model(app_label, model_name)
    person_model = apps.get_model("rekisteri", "Person")
    backfill_profiles(user_model, person_model)


class Migration(migrations.Migration):
    """Every account gets the matrikkeli profile it should always have had.

    The post-save signal only fires on creation, so accounts that predate it
    keep the gap it was written to close: matrikkeli views read ``user.person``
    and raise ``Person.DoesNotExist`` for anyone without one.

    Reversing is a noop. A profile carries data of its own once someone edits
    it, and there is nothing here worth deleting it over.
    """

    dependencies = [
        ("rekisteri", "0003_person_pora_member"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
