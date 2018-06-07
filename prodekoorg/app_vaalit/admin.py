from django.contrib import admin
from django.db import models
from prodekoorg.app_vaalit.models import Ehdokas, Kysymys, Virka, Vastaus


class VirkaAdmin(admin.ModelAdmin):
    pass


class EhdokasAdmin(admin.ModelAdmin):
    list_display = ('name', )


class KysymysAdmin(admin.ModelAdmin):
    list_display = ('to_virka', 'created_at')


class VastausAdmin(admin.ModelAdmin):
    list_display = ('to_question', 'created_at')


admin.site.register(Virka, VirkaAdmin)
admin.site.register(Ehdokas, EhdokasAdmin)
admin.site.register(Kysymys, KysymysAdmin)
admin.site.register(Vastaus, VastausAdmin)
