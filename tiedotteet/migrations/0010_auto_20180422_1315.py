# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-22 13:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiedotteet', '0009_auto_20180419_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='deadline_date',
            field=models.DateField(blank=True, default=datetime.date(2018, 4, 29), null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='end_date',
            field=models.DateField(default=datetime.date(2018, 4, 29)),
        ),
    ]
