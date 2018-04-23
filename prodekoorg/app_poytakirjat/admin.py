from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from prodekoorg.app_poytakirjat.models import Dokumentti


class YearFilter(SimpleListFilter):
    title = 'vuosi'
    parameter_name = 'vuosi'

    def lookups(self, request, model_admin):
        years = set([d.date.year for d in model_admin.model.objects.all()])
        return [(y, y) for y in years]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(date__year=self.value())
        else:
            return queryset


class DokumenttiAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_filter = (YearFilter,)


admin.site.register(Dokumentti, DokumenttiAdmin)
