import csv

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from .models import HallituksenJasen, Jaosto, Toimari


class YearFilter(SimpleListFilter):
    title = _("year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        years = set([m.year for m in model_admin.model.objects.all()])
        return [(y, y) for y in years]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(year=self.value())
        else:
            return queryset


def exportcsv(modeladmin, request, queryset):
    """Handle a CSV POST request and create new Guild Official objects.

    Args:
        modeladmin: Django's representation of a model in admin panel
        request: HttpRequest object from Django.
        queryset: Represents selected (Toimari) objects in admin panel

    Returns:
        If user is logged in and has staff permissions, a CSV containg
        all 'Toimari' objects will be returned.

        Otherwise a permission denied exception will be raised.
    """

    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment;filename=toimarit.csv"
    writer = csv.writer(response, delimiter=";")
    field_names = [field.name for field in opts.fields]
    field_names = field_names[1:]

    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


@admin.register(Jaosto)
class JaostoAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Toimari)
class ToimariAdmin(admin.ModelAdmin):
    list_display = ("year", "firstname", "lastname", "section", "position")
    list_filter = (YearFilter,)

    actions = [exportcsv]
    exportcsv.short_description = _("Export selected as CSV")


@admin.register(HallituksenJasen)
class HallituksenJasenAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "firstname",
        "lastname",
        "position",
        "position_eng",
        "section",
        "mobilephone",
        "email",
    )
    list_filter = (YearFilter,)

    actions = [exportcsv]
    exportcsv.short_description = _("Export selected as CSV")
