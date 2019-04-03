# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 08:45
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kulukorvaus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('target', models.CharField(max_length=50, verbose_name='Expense explanation')),
                ('explanation', models.CharField(max_length=100, verbose_name='Event / expense target')),
                ('sum_euros', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Sum (in €)')),
                ('additional_info', models.TextField(blank=True, verbose_name='Additional information')),
                ('receipt', models.FileField(upload_to='kulukorvaukset/%Y-%m', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Receipt')),
            ],
            options={
                'verbose_name': 'reimbursement',
                'verbose_name_plural': 'Reimbursements',
            },
        ),
        migrations.CreateModel(
            name='KulukorvausPerustiedot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_by', models.CharField(max_length=50, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('position_in_guild', models.CharField(choices=[('H', 'Board'), ('T', 'Guild official')], max_length=12, verbose_name='Position in guild')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone number')),
                ('bank_number', models.CharField(max_length=32, verbose_name='Account number (IBAN)')),
                ('bic', models.CharField(choices=[('OP', 'OKOYFIHH'), ('NORDEA', 'NDEAFIHH'), ('SPANKKI', 'SBANFIHH'), ('DANSKE', 'DABAFIHH'), ('HANDELS', 'HANDFIHH')], max_length=11, verbose_name='BIC')),
                ('sum_overall', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total reimbursement (in €)')),
                ('additional_info', models.TextField(blank=True, verbose_name='Additional information')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='kulukorvaukset/%Y-%m', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='PDF')),
                ('created_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reimbursement basic information',
                'verbose_name_plural': 'Reimbursement basic information',
            },
        ),
        migrations.AddField(
            model_name='kulukorvaus',
            name='info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_kulukorvaus.KulukorvausPerustiedot'),
        ),
    ]
