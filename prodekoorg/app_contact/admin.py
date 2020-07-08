from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from .models import Message


class YearFilter(SimpleListFilter):
    title = _("year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        years = set([d.created_at.year for d in model_admin.model.objects.all()])
        return [(y, y) for y in years]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(created_at__year=self.value())
        else:
            return queryset


class MessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "email", "message")
    list_filter = (YearFilter,)

    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 8, "cols": 1})
        }  # Override Textarea default height
    }


admin.site.register(Message, MessageAdmin)
