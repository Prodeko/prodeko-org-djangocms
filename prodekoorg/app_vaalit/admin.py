from django.contrib import admin

from .models import Ehdokas, Kysymys, Vastaus, Virka


class VirkaAdmin(admin.ModelAdmin):
    def make_visible(modeladmin, request, queryset):
        queryset.update(is_visible=True)

    def make_hidden(modeladmin, request, queryset):
        queryset.update(is_visible=False)

    make_visible.short_description = "Mark selected items as visible"
    make_hidden.short_description = "Mark selected items as hidden"
    actions = [make_visible, make_hidden]
    list_display = ('name', 'sort_key', 'is_board', 'is_visible')



class EhdokasAdmin(admin.ModelAdmin):
    list_display = ("name", "virka")


class KysymysAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    list_display = ("to_virka", "created_at")


class VastausAdmin(admin.ModelAdmin):
    list_display = ("to_question", "created_at")


admin.site.register(Virka, VirkaAdmin)
admin.site.register(Ehdokas, EhdokasAdmin)
admin.site.register(Kysymys, KysymysAdmin)
admin.site.register(Vastaus, VastausAdmin)
