from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from .models import Tapahtuma


class YearFilter(SimpleListFilter):
    title = _("year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        years = set([str(d.start_date.year) + '/' + str(d.start_date.month).zfill(2) for d in model_admin.model.objects.all()])
        return [(y, y) for y in years]

    def queryset(self, request, queryset):
        if self.value() is not None:
            (year, month) = self.value().split('/')
            return queryset.filter(date__month=int(month), date__year=int(year))
        else:
            return queryset


class TapahtumaAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "state")
    list_filter = (YearFilter,)


admin.site.register(Tapahtuma, TapahtumaAdmin)
