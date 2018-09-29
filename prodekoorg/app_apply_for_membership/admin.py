from django.contrib import admin
from django.db import models
from django.forms import Textarea
from prodekoorg.app_apply_for_membership.models import (PendingUser)


class PendingUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'hometown')

    # Override Textarea default height
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 1})},
    }


admin.site.register(PendingUser, PendingUserAdmin)