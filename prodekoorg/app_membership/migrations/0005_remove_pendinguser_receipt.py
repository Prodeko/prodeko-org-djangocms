# Generated by Django 3.1.4 on 2024-01-03 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_membership', '0004_pendinguser_has_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendinguser',
            name='receipt',
        ),
    ]
