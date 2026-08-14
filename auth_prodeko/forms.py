from django import forms


class EditProfileForm(forms.Form):
    """Email only. Passwords and names live in the Prodeko account."""

    email = forms.EmailField(label="Email", max_length=50, required=False)
