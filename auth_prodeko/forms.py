from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class EditProfileForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, required=False)
    newpassword = forms.CharField(widget=forms.PasswordInput(
    ), label='New Password', max_length=50, required=False)
    newpassword_confirm = forms.CharField(widget=forms.PasswordInput(
    ), label='Confirm New Password', max_length=50, required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(), label='Current Password', max_length=50)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not check_password(password, self.user.password):
            self.add_error('password', _('Incorrect password'))

    def clean(self):
        cleaned_data = super().clean()
        newpassword = cleaned_data.get('newpassword')
        newpassword_confirm = cleaned_data.get('newpassword_confirm')

        if newpassword or newpassword_confirm:
            errors = []
            password_validators = get_default_password_validators()
            for validator in password_validators:
                try:
                    validator.validate(newpassword, self.user)
                except ValidationError as error:
                    errors.append(error)
            for error in errors:
                self.add_error('newpassword', error)

            if newpassword_confirm != newpassword:
                self.add_error('newpassword', _('Passwords don\'t match'))
                self.add_error('newpassword_confirm',
                               _('Passwords don\'t match'))
