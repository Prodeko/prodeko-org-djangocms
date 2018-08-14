from functools import update_wrapper

from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from prodekoorg.app_toimarit import views
from prodekoorg.app_toimarit.models import *
import csv

from .models import Toimari, HallituksenJasen


def exportcsv(modeladmin, request, queryset):
    if not request.user.is_staff:	
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=toimarit.csv'
    writer = csv.writer(response, delimiter=';')
    field_names = [field.name for field in opts.fields]
    field_names = field_names[1:]

    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

@admin.register(Toimari)
class ToimariAdmin(admin.ModelAdmin):
    list_display = ('etunimi', 'sukunimi', 'virka')
    actions = [exportcsv]
    exportcsv.short_description="Export selected as CSV"

@admin.register(HallituksenJasen)
class HallituksenJasenAdmin(admin.ModelAdmin):
    list_display = ('etunimi', 'sukunimi', 'virka', 'virka_eng', 'jaosto', 'puhelin', 'sahkoposti')
    actions = [exportcsv]
    exportcsv.short_description="Export selected as CSV"