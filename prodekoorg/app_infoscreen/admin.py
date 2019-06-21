from django.contrib import admin
from .models import Slide


class SlideAdmin(admin.ModelAdmin):
    list_display = ["title"]


admin.site.register(Slide, SlideAdmin)
