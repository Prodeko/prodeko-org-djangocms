# Generated by Django 3.1.4 on 2024-01-03 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_proleko', '0004_auto_20231107_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lehti',
            name='year',
            field=models.IntegerField(default=2024, verbose_name='Year'),
        ),
    ]
