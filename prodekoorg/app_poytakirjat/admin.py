from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .gdrive_api import run_app_poytakirjat
from .models import Dokumentti


class YearFilter(SimpleListFilter):
    title = _("year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        years = set([d.date.year for d in model_admin.model.objects.all()])
        return [(y, y) for y in years]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(date__year=self.value())
        else:
            return queryset


class DokumenttiAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        app_poytakirjat_urls = [
            path("download", run_app_poytakirjat, name="download_docs_from_gsuite",),
        ]
        return app_poytakirjat_urls + urls

    list_display = ("name", "date")
    list_filter = (YearFilter,)


admin.site.register(Dokumentti, DokumenttiAdmin)
