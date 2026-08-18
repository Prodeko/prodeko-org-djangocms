from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "has_accepted_policies",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Keycloak"),
            {"fields": ("keycloak_sub", "keycloak_linked_at", "predates_keycloak")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    readonly_fields = ("keycloak_sub", "keycloak_linked_at")
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "has_accepted_policies",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    actions = ["unlink_from_keycloak"]

    @admin.action(
        description=_("Unlink the selected accounts from Keycloak"),
        permissions=["change"],
    )
    def unlink_from_keycloak(self, request, queryset):
        """Undo a link the sign-in path will not undo by itself.

        A Keycloak user deleted and created again at the same address
        gets a new subject, and the account here still names the old one,
        so every sign-in is refused with a message telling whoever reads
        the log to resolve it by hand. This is that hand: the next sign-in
        links the account afresh.

        An action rather than an editable field, because clearing the
        subject is the whole of the useful operation and typing one in
        wrong would hand someone else's identity an account.
        """
        updated = queryset.update(keycloak_sub=None, keycloak_linked_at=None)
        self.message_user(
            request,
            ngettext(
                "%d account was unlinked from Keycloak. Its next sign-in "
                "links it again.",
                "%d accounts were unlinked from Keycloak. Their next sign-in "
                "links them again.",
                updated,
            )
            % updated,
        )
