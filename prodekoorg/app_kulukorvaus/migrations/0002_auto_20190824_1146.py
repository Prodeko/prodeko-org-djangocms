# Generated by Django 2.1.10 on 2019-08-24 11:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_kulukorvaus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kulukorvausperustiedot',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='./kulukorvaukset/%Y-%m', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='PDF'),
        ),
    ]
