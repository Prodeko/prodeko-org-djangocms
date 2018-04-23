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

from .models import Toimari



@admin.register(Toimari)
class ToimariAdmin(admin.ModelAdmin):
    list_display = ('etunimi', 'sukunimi', 'virka', 'virka_eng', 'jaosto', 'puhelin', 'sahkoposti')
