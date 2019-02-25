# -*- coding: utf-8 -*-

from django.contrib.admin.widgets import AdminDateWidget
from django.forms import (CharField, CheckboxInput, Form, ModelForm,
                          NumberInput, PasswordInput, Select, SelectMultiple,
                          Textarea, TextInput)
from django.utils.translation import ugettext_lazy as _
from tiedotteet.info.models import Category, MailConfiguration, Message, Tag


class PublishForm(ModelForm):
    class Meta:
        model = Message
        fields = ['header', 'content', 'category', 'tags', 'start_date',
                  'end_date', 'deadline_date', 'show_deadline', 'visible']
        labels = {
            'header': _('Header'),
            'content': _('Content'),
            'category': _('Category'),
            'tags': _('Tags'),
            'start_date': _('Start date'),
            'end_date': _('End date'),
            'deadline_date': _('Deadline'),
            'show_deadline': _('Show deadline'),
            'visible': _('Visible'),
        }
        widgets = {
            'header': TextInput(attrs={'class': 'form-control input-md'}),
            'content': Textarea(attrs={'id': 'foo'}),
            'start_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
            'end_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
            'deadline_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
            'category': Select(attrs={'class': 'form-control'}),
            'tags': SelectMultiple(attrs={'class': 'form-control'}),
            'show_deadline': CheckboxInput(),
            'visible': CheckboxInput(),
        }


class EditForm(ModelForm):
    class Meta:
        model = Message
        success_message = _('Bulletin updated')
        fields = ['header', 'content', 'category', 'tags', 'start_date',
                  'end_date', 'deadline_date', 'show_deadline', 'visible']
        labels = {
            'header': _('Header'),
            'content': _('Content'),
            'category': _('Category'),
            'tags': _('Tags'),
            'start_date': _('Start date'),
            'end_date': _('End date'),
            'deadline_date': _('Deadline'),
            'show_deadline': _('Show deadline'),
            'visible': _('Visible'),
        }
        widgets = {
            'header': TextInput(attrs={'class': 'form-control input-md'}),
            'content': Textarea(attrs={'id': 'foo'}),
            'start_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
            'end_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
            'deadline_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
            'category': Select(attrs={'class': 'form-control'}),
            'tags': SelectMultiple(attrs={'class': 'form-control'}),
            'show_deadline': CheckboxInput(),
            'visible': CheckboxInput(),
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'order', 'login_required']
        labels = {
            'title': _('Category'),
            'order': _('Order'),
            'login_required': _('Visibility'),
        }
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'order': NumberInput(attrs={'class': 'form-control'}),
            'login_required': Select(attrs={'class': 'form-control'}, choices=((False, _("Public")), (True, _("Login required"))))
        }


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        labels = {
            'title': _('Add a new tag'),
        }
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
        }


class MailConfigurationForm(ModelForm):
    class Meta:
        model = MailConfiguration
        fields = ['host', 'port', 'username', 'password', 'use_tls']
        labels = {
            'host': _('Host'),
            'port': _('Port'),
            'username': _('Username (email)'),
            'password': _('Password'),
            'use_tls': _('Use TLS Encryption'),
        }
        widgets = {
            'host': TextInput(attrs={'class': 'form-control'}),
            'port': NumberInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'use_tls': CheckboxInput(),
        }


class SendEmailForm(Form):
    subject = CharField(widget=TextInput(
        attrs={'class': 'form-control'}), label=_("Title"))
    to = CharField(widget=TextInput(
        attrs={'class': 'form-control'}), label=_("Recipients (separated by comma)"))
