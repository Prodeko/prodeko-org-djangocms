# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150, blank=True, null=True)),
                ('order', models.IntegerField(default=0, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=datetime.date(2016, 9, 18))),
                ('deadline_date', models.DateField(default=datetime.date(2016, 9, 18), blank=True, null=True)),
                ('show_deadline', models.BooleanField(default=False)),
                ('visible', models.BooleanField(default=True)),
                ('category', models.ForeignKey(to='info.Category', related_name='messages', null=True)),
            ],
        ),
    ]
