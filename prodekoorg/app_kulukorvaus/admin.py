from django.contrib import admin
from prodekoorg.app_kulukorvaus.models import Kulukorvaus

from django.contrib.admin import SimpleListFilter


class YearFilter(SimpleListFilter):
    title = 'vuosi'
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
    list_display = ('created_at', 'created_by', 'explanation')
    # list_filter = (YearFilter,)


admin.site.register(Kulukorvaus, KulukorvausAdmin)
