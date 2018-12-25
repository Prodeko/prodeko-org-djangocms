from django.conf.urls import url
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms import Textarea
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _
from prodekoorg.app_apply_for_membership.models import PendingUser


class PendingUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user',
                    'hometown', 'application_actions')

    formfield_overrides = {
        # Override Textarea default height
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 1})},
    }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<account_id>.+)/view/$',
                self.admin_site.admin_view(view_application),
                name='application-view',
            ),
            url(
                r'^(?P<account_id>.+)/accept/$',
                self.admin_site.admin_view(accept_application),
                name='application-accept',
            ),
            url(
                r'^(?P<account_id>.+)/reject/$',
                self.admin_site.admin_view(reject_application),
                name='application-reject',
            ),
        ]
        return custom_urls + urls

    def application_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">' + _('View') + '</a>&nbsp;'
            '<a class="button" href="{}">' + _('Accept') + '</a>&nbsp;'
            '<a class="button" href="{}">' + _('Reject') + '</a>',
            reverse('admin:application-view', args=[obj.pk]),
            reverse('admin:application-accept', args=[obj.pk]),
            reverse('admin:application-reject', args=[obj.pk]),
        )
    application_actions.short_description = _('Application actions')
    application_actions.allow_tags = True


admin.site.register(PendingUser, PendingUserAdmin)


def view_application(request, account_id, *args, **kwargs):
    if not request.user.is_staff:
        raise PermissionDenied
    return redirect("../")


def accept_application(request, account_id, *args, **kwargs):
    if not request.user.is_staff:
        raise PermissionDenied
    user = PendingUser.objects.get(pk=account_id)
    user.accept_membership(request, args, kwargs)
    return redirect("../../")


def reject_application(request, account_id, *args, **kwargs):
    if not request.user.is_staff:
        raise PermissionDenied
    user = PendingUser.objects.get(pk=account_id)
    user.reject_membership(request, args, kwargs)
    return redirect("../../")
