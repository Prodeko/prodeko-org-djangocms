from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User


class EditProfileForm(forms.Form):
    """Email only. Passwords and names live in the Prodeko account."""

    email = forms.EmailField(label="Email", max_length=50, required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        """User.email is unique, so a taken address must be a form error."""
        email = self.cleaned_data["email"]
        if not email:
            return email
        taken = User.objects.filter(email__iexact=email)
        if self.user.pk is not None:
            taken = taken.exclude(pk=self.user.pk)
        if taken.exists():
            raise forms.ValidationError(
                _("An account with that email address already exists.")
            )
        return email
