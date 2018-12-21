from django.forms import ModelForm, RadioSelect, Textarea
from django.utils.translation import ugettext_lazy as _

from .models import PendingUser


class PendingUserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PendingUserForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

        if 'membership_type' in self.fields:
            self.fields['membership_type'].widget = RadioSelect(
                choices=PendingUser.MEMBERSHIP_TYPE_CHOICES)
        if 'is_ayy_member' in self.fields:
            self.fields['is_ayy_member'].widget = RadioSelect(
                choices=PendingUser.AYY_MEMBER_CHOICES)
        for visible in self.visible_fields():
            if visible.name not in ['membership_type', 'is_ayy_member']:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = PendingUser
        exclude = ['created_by_user']
        widgets = {
            'additional_info': Textarea(attrs={'rows': 4, 'cols': 1}),
        }
        help_texts = {
            'membership_type': _('If you are studying at Aalto apply as a true member. Otherwise, apply as external member.'),
        }
