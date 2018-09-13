from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from django.forms import Textarea
from prodekoorg.app_kulukorvaus.models import (Kulukorvaus,
                                               KulukorvausPerustiedot)


class YearFilter(SimpleListFilter):
    title = 'Vuosi'
    parameter_name = 'vuosi'

    def lookups(self, request, model_admin):
        years = set([d.created_at.year for d in model_admin.model.objects.all()])
        return [(y, y) for y in years]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(created_at__year=self.value())
        else:
            return queryset


class KulukorvausAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'explanation')
    list_filter = (YearFilter,)

    # Override Textarea default height
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 1})},
    }


class KulukorvausPerustiedotAdmin(admin.ModelAdmin):
    # Override Textarea default height
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 1})},
    }


admin.site.register(Kulukorvaus, KulukorvausAdmin)
admin.site.register(KulukorvausPerustiedot, KulukorvausPerustiedotAdmin)
