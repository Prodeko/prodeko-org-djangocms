# Generated by Django 3.1.4 on 2023-09-19 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rekisteri', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workexperience',
            name='is_founding_member',
            field=models.BooleanField(default=False),
        ),
    ]
