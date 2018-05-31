from django.contrib import admin
from django.db import models
from prodekoorg.app_vaalit.models import Ehdokas, Kysymys, Virka


class VirkaAdmin(admin.ModelAdmin):
    pass


class EhdokasAdmin(admin.ModelAdmin):
    list_display = ('name', )


class KysymysAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'to_applicant')


admin.site.register(Virka, VirkaAdmin)
admin.site.register(Ehdokas, EhdokasAdmin)
admin.site.register(Kysymys, KysymysAdmin)
