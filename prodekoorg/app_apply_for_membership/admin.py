from django.conf.urls import url
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import Textarea
<<<<<<< HEAD
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from prodekoorg.app_apply_for_membership.models import PendingUser
=======
from django.shortcuts import redirect
from django.utils.html import format_html
from prodekoorg.app_apply_for_membership.models import (PendingUser)
>>>>>>> 36bcc6987430efa281571ff292e2b308ae8091ba

class PendingUserAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('first_name', 'last_name',
                    'hometown', 'application_actions')
=======
    list_display = ('first_name', 'last_name', 'user', 'hometown', 'application_actions')
>>>>>>> 36bcc6987430efa281571ff292e2b308ae8091ba

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
<<<<<<< HEAD
                name='account-view',
=======
                name='application-view',
>>>>>>> 36bcc6987430efa281571ff292e2b308ae8091ba
            ),
            url(
                r'^(?P<account_id>.+)/accept/$',
                self.admin_site.admin_view(acceptApplication),
<<<<<<< HEAD
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
=======
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
>>>>>>> 36bcc6987430efa281571ff292e2b308ae8091ba
