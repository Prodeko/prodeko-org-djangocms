from django.conf.urls import url
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import Textarea
from django.shortcuts import redirect
from django.utils.html import format_html
from prodekoorg.app_apply_for_membership.models import PendingUser


class PendingUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user',
                    'hometown', 'application_actions')

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
                name='application-view',
            ),
            url(
                r'^(?P<account_id>.+)/accept/$',
                self.admin_site.admin_view(acceptApplication),
                name='application-accept',
            ),
            url(
                r'^(?P<account_id>.+)/reject/$',
                self.admin_site.admin_view(rejectApplication),
                name='application-reject',
            ),
        ]
        return custom_urls + urls

    def application_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">View</a>&nbsp;'
            '<a class="button" href="{}">Accept</a>&nbsp;'
            '<a class="button" href="{}">Reject</a>',
            reverse('admin:application-view', args=[obj.pk]),
            reverse('admin:application-accept', args=[obj.pk]),
            reverse('admin:application-reject', args=[obj.pk]),
        )
    application_actions.short_description = 'Application actions'
    application_actions.allow_tags = True


admin.site.register(PendingUser, PendingUserAdmin)


def viewApplication(request, account_id, *args, **kwargs):
    if not request.user.is_staff:
        raise PermissionDenied
    return redirect("../")


def acceptApplication(request, account_id, *args, **kwargs):
    if not request.user.is_staff:
        raise PermissionDenied
    user = PendingUser.objects.get(pk=account_id)
    user.acceptMembership(request, args, kwargs)
    return redirect("../../")


def rejectApplication(request, account_id, *args, **kwargs):
    if not request.user.is_staff:
        raise PermissionDenied
    user = PendingUser.objects.get(pk=account_id)
    user.rejectMembership(request, args, kwargs)
    return redirect("../../")
