from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.forms import Textarea
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from .constants import MAILING_LIST_PORA, MAILING_LIST_PRODEKO
from .groups_api import main_groups_api
from .models import PendingUser


class PendingUserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "user",
        "hometown",
        "application_actions",
    )

    formfield_overrides = {
        # Override Textarea default height
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 1})}
    }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<account_id>/view/",
                self.admin_site.admin_view(view_application),
                name="application-view",
            ),
            path(
                "<account_id>/accept/",
                self.admin_site.admin_view(accept_application),
                name="application-accept",
            ),
            path(
                "<account_id>/reject/",
                self.admin_site.admin_view(reject_application),
                name="application-reject",
            ),
        ]
        return custom_urls + urls

    def application_actions(self, obj):
        """Add a set of three buttons to Django admin

        Buttons are added to the row which displays a PendingUser model.
        """
        return format_html(
            '<a class="button" href="{}">' + _("View") + "</a>&nbsp;"
            '<a class="button btn-accept-membership" href="{}">'
            + _("Accept")
            + "</a>&nbsp;"
            '<a class="button btn-reject-membership" href="{}">' + _("Reject") + "</a>",
            reverse("admin:application-view", args=[obj.pk]),
            reverse("admin:application-accept", args=[obj.pk]),
            reverse("admin:application-reject", args=[obj.pk]),
        )

    application_actions.short_description = _("Application actions")
    application_actions.allow_tags = True


admin.site.register(PendingUser, PendingUserAdmin)


@staff_member_required
def view_application(request, account_id, *args, **kwargs):
    """View a membership application from Django admin."""
    return redirect("/fi/admin/app_membership/pendinguser/")


@staff_member_required
def accept_application(request, account_id, *args, **kwargs):
    """Accept a membership application from Django admin."""
    user = PendingUser.objects.get(pk=account_id)
    user.accept_membership(request, args, kwargs)
    main_groups_api(request, user.email, MAILING_LIST_PRODEKO)
    if user.language == "FI":
        main_groups_api(request, user.email, MAILING_LIST_PORA)
    return redirect("/fi/admin/app_membership/pendinguser/")


@staff_member_required
def reject_application(request, account_id, *args, **kwargs):
    """Reject a membership application from Django admin."""
    user = PendingUser.objects.get(pk=account_id)
    user.reject_membership(request, args, kwargs)
    return redirect("/fi/admin/app_membership/pendinguser/")
