# Generated by Django 2.1.10 on 2019-09-05 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_kulukorvaus', '0002_kulukorvausperustiedot_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kulukorvausperustiedot',
            name='position_in_guild',
        ),
    ]
