from django.forms import ModelForm, RadioSelect, Textarea, HiddenInput
from django.utils.translation import ugettext_lazy as _

from .models import PendingUser
from auth_prodeko.models import User


class PendingUserForm(ModelForm):
    """PendingUserForm class extending Django's ModelForm.

    Maps PendingUser model's fields to HTML form <input> elements.
    """

    def __init__(self, *args, **kwargs):
        super(PendingUserForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

        if 'language' in self.fields:
            self.fields['language'].widget = RadioSelect(
                choices=PendingUser.LANGUAGE_CHOICES)
        if 'membership_type' in self.fields:
            self.fields['membership_type'].widget = RadioSelect(
                choices=PendingUser.MEMBERSHIP_TYPE_CHOICES)
        if 'is_ayy_member' in self.fields:
            self.fields['is_ayy_member'].widget = RadioSelect(
                choices=PendingUser.AYY_MEMBER_CHOICES)
        for visible in self.visible_fields():
            if visible.name not in ['language', 'membership_type', 'is_ayy_member']:
                visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        # Verify that the email doesn't already exist
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error('email', _("An application or account associated with this email already exists"))

    class Meta:
        model = PendingUser
        exclude = ['created_by_user']
        widgets = {
            'additional_info': Textarea(attrs={'rows': 4, 'cols': 1}),
            'has_accepted_policies': HiddenInput()
        }
        help_texts = {
            'membership_type': _('If you are studying at Aalto apply as a true member. Otherwise, apply as external member.'),
        }
