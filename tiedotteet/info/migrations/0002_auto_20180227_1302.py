# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('host', models.CharField(default='mail.aalto.fi', max_length=50)),
                ('port', models.CharField(default='587', max_length=10)),
                ('username', models.CharField(default='tiedottaja@aalto.fi', max_length=50)),
                ('password', models.CharField(default='salasana', max_length=50)),
                ('use_tls', models.BooleanField(default=True)),
                ('fail_silently', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(null=True, blank=True, max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='login_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='deadline_date',
            field=models.DateField(null=True, blank=True, default=datetime.date(2018, 3, 6)),
        ),
        migrations.AlterField(
            model_name='message',
            name='end_date',
            field=models.DateField(default=datetime.date(2018, 3, 6)),
        ),
        migrations.AddField(
            model_name='message',
            name='tags',
            field=models.ManyToManyField(related_name='messages', to='info.Tag', null=True, blank=True),
        ),
    ]
