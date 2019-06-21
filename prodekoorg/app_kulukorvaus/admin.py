from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from .models import Kulukorvaus, KulukorvausPerustiedot


class YearFilter(SimpleListFilter):
    """Filter for Django admin to"""

    title = _("Year")
    parameter_name = "vuosi"

    def lookups(self, request, model_admin):
        """Allows filtering the reimbursements by year in Django admin"""
        years = set([d.created_at.year for d in model_admin.model.objects.all()])
        return [(y, y) for y in years]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(created_at__year=self.value())
        else:
            return queryset


class KulukorvausAdmin(admin.ModelAdmin):
    list_display = ("created_at", "explanation")
    list_filter = (YearFilter,)

    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 1, "cols": 1})
        }  # Override Textarea default height
    }


class KulukorvausPerustiedotAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 1, "cols": 1})
        }  # Override Textarea default height
    }


admin.site.register(Kulukorvaus, KulukorvausAdmin)
admin.site.register(KulukorvausPerustiedot, KulukorvausPerustiedotAdmin)
