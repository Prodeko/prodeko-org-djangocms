import csv

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from .models import HallituksenJasen, Jaosto, Toimari


def exportcsv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=toimarit.csv'
    writer = csv.writer(response, delimiter=';')
    field_names = [field.name for field in opts.fields]
    field_names = field_names[1:]

    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


@admin.register(Jaosto)
class JaostoAdmin(admin.ModelAdmin):
    list_display = ('nimi', )


@admin.register(Toimari)
class ToimariAdmin(admin.ModelAdmin):
    list_display = ('etunimi', 'sukunimi', 'jaosto', 'virka')
    actions = [exportcsv]
    exportcsv.short_description = _('Export selected as CSV')


@admin.register(HallituksenJasen)
class HallituksenJasenAdmin(admin.ModelAdmin):
    list_display = ('etunimi', 'sukunimi', 'virka', 'virka_eng',
                    'jaosto', 'puhelin', 'sahkoposti')
    actions = [exportcsv]
    exportcsv.short_description = _('Export selected as CSV')
