from django.contrib import admin
from .models import Toimari
from django import forms
from django.http import HttpResponse
from django.conf.urls import url

from django.contrib.admin import AdminSite
from prodekoorg.app_toimarit import views
from functools import update_wrapper
from django.template import RequestContext  
from django.shortcuts import render_to_response

from prodekoorg.app_toimarit.models import *

# Register your models here.

@admin.register(Toimari)
class ToimariAdmin(admin.ModelAdmin):
	list_display = ('etunimi', 'sukunimi', 'virka', 'virka_eng', 'jaosto', 'puhelin', 'sahkoposti')