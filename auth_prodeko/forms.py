from django import forms
from django.contrib.auth.hashers import check_password


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
        password = self.cleaned_data.get("password")
        if not check_password(password, self.user.password):
            self.add_error('password', "Incorrect password")

    def clean(self):
        cleaned_data = super().clean()
        newpassword = cleaned_data.get("newpassword")
        newpassword_confirm = cleaned_data.get("newpassword_confirm")

        if newpassword:
            if newpassword_confirm != newpassword:
                self.add_error('newpassword_confirm', "Passwords don't match")
