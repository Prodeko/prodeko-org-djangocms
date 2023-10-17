from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from .forms import MyActionForm
from .models import Ehdokas, Kysymys, Vastaus, Virka


class VirkaAdmin(admin.ModelAdmin):
    def make_visible(modeladmin, request, queryset):
        queryset.update(is_visible=True)

    def make_hidden(modeladmin, request, queryset):
        queryset.update(is_visible=False)

    make_visible.short_description = "Mark selected items as visible"
    make_hidden.short_description = "Mark selected items as hidden"

        
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('set-date/', self.set_date_view, name='set-date'),
        ]
        return custom_urls + urls

    def set_date(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        selected_str = ','.join(str(pk) for pk in selected)
        return HttpResponseRedirect(f'/admin/app_vaalit/virka/set-date/?ids={selected_str}')
    
    set_date.short_description = "Set application start date"
    actions = [make_visible, make_hidden, set_date]
    list_display = ('name', 'sort_key', 'application_start', 'is_hallitus', 'is_visible')

    def set_date_view(self, request):
        selected_str = request.GET.get('ids')
        selected = Virka.objects.filter(pk__in=selected_str.split(','))

        if request.method == 'POST':
            form = MyActionForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                selected.update(application_start=form.cleaned_data['date'])
                self.message_user(request, 'Action completed')
                return HttpResponseRedirect('/admin/app_vaalit/virka/')
        else:
            form = MyActionForm()

        return render(request, 'admin/admin_set_date_form.html', {'form': form})


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
