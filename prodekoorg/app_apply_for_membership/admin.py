from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from prodekoorg.app_apply_for_membership.models import (PendingUser)

class PendingUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'hometown', 'application_actions')

    # Override Textarea default height
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 1})},
    }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<account_id>.+)/view/$',
                self.admin_site.admin_view(viewApplication),
                name='account-view',
            ),
            url(
                r'^(?P<account_id>.+)/accept/$',
                self.admin_site.admin_view(acceptApplication),
                name='account-accept',
            ),
            url(
                r'^(?P<account_id>.+)/decline/$',
                self.admin_site.admin_view(acceptApplication),
                name='account-decline',
            ),
        ]
        return custom_urls + urls

    def application_actions(self, obj):
    	return format_html(
    		'<a class="button" href="{}">View</a>&nbsp;'
            '<a class="button" href="{}">Accept</a>&nbsp;'
            '<a class="button" href="{}">Decline</a>',
            reverse('admin:account-view', args=[obj.pk]),
            reverse('admin:account-accept', args=[obj.pk]),
            reverse('admin:account-decline', args=[obj.pk]),
        )
    application_actions.short_description = 'Application actions'
    application_actions.allow_tags = True

admin.site.register(PendingUser, PendingUserAdmin)

def viewApplication(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    return redirect("../")

def acceptApplication(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    return response


def declineApplication(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    return response