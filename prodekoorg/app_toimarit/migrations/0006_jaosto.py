# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-04 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_toimarit', '0005_auto_20180814_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jaosto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=50)),
            ],
        ),
    ]