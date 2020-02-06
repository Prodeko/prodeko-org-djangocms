import csv

from django.contrib import admin
from django.urls import include, re_path, path
from django.views.generic import TemplateView
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from .models import HallituksenJasen, Jaosto, Toimari
from .views import toimari_postcsv, hallitus_postcsv


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
        queryset: Represents selected objects in admin panel

    Returns:
        If user is logged in and has staff permissions, a CSV containg
        all objects will be returned.

        Otherwise a permission denied exception will be raised.
    """

    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment;filename=data.csv"
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
    def get_urls(self):
        urls = super().get_urls()
        toimari_urls = [
            path(
                "csvupload",
                TemplateView.as_view(
                    template_name="admin/app_toimarit/toimari/uploadcsv.html"
                ),
                name="upload_toimari_csv",
            ),
            path("postcsv", toimari_postcsv, name="toimari_postcsv"),
        ]
        return toimari_urls + urls

    list_display = ("year", "firstname", "lastname", "section", "position")
    list_filter = (YearFilter,)

    actions = [exportcsv]
    exportcsv.short_description = _("Export selected as CSV")


@admin.register(HallituksenJasen)
class HallituksenJasenAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        hallitus_urls = [
            path(
                "csvupload",
                TemplateView.as_view(
                    template_name="admin/app_toimarit/hallituksenjasen/uploadcsv.html"
                ),
                name="upload_hallitus_csv",
            ),
            path("postcsv", hallitus_postcsv, name="hallitus_postcsv"),
        ]
        return hallitus_urls + urls

    list_display = (
        "year",
        "firstname",
        "lastname",
        "position_fi",
        "position_en",
        "mobilephone",
        "email",
    )
    list_filter = (YearFilter,)

    actions = [exportcsv]
    exportcsv.short_description = _("Export selected as CSV")
