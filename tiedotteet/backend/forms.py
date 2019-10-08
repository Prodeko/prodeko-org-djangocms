# -*- coding: utf-8 -*-

from ckeditor.widgets import CKEditorWidget
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import (CharField, CheckboxInput, Form, ModelForm,
                          NumberInput, PasswordInput, Select, SelectMultiple,
                          Textarea, TextInput)
from django.utils.translation import ugettext_lazy as _
from tiedotteet.backend.models import (Category, MailConfiguration,
                                                  Message, Tag)


class PublishForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Overrides the ModelForm __init__ method.

        This way we can attach widgets and bootstrap classess
        to certain form fields to make them look better in the UI.
        Same technique is used for other forms below.
        """

        # Call ModelForm __init__ method.
        super(PublishForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if visible.name not in ["show_deadline", "visible"]:
                # 'form-control' is a bootstrap class used to style
                # form fields appropriately.
                visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Message
        fields = [
            "header",
            "content",
            "category",
            "tags",
            "start_date",
            "end_date",
            "deadline_date",
            "show_deadline",
            "visible",
        ]
        labels = {
            "header": _("Header"),
            "content": _("Content"),
            "category": _("Category"),
            "tags": _("Tags"),
            "start_date": _("Start date"),
            "end_date": _("End date"),
            "deadline_date": _("Deadline"),
            "show_deadline": _("Show deadline"),
            "visible": _("Visible"),
        }
        widgets = {
            "header": TextInput(),
            "content": CKEditorWidget(),
            "start_date": AdminDateWidget(),
            "end_date": AdminDateWidget(),
            "deadline_date": AdminDateWidget(),
            "category": Select(),
            "tags": SelectMultiple(),
            "show_deadline": CheckboxInput(),
            "visible": CheckboxInput(),
        }


class EditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if visible.name not in ["show_deadline", "visible"]:
                visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Message
        success_message = _("Bulletin updated")
        fields = [
            "header",
            "content",
            "category",
            "tags",
            "start_date",
            "end_date",
            "deadline_date",
            "show_deadline",
            "visible",
        ]
        labels = {
            "header": _("Header"),
            "content": _("Content"),
            "category": _("Category"),
            "tags": _("Tags"),
            "start_date": _("Start date"),
            "end_date": _("End date"),
            "deadline_date": _("Deadline"),
            "show_deadline": _("Show deadline"),
            "visible": _("Visible"),
        }
        widgets = {
            "header": TextInput(),
            "content": CKEditorWidget(),
            "start_date": AdminDateWidget(),
            "end_date": AdminDateWidget(),
            "deadline_date": AdminDateWidget(),
            "category": Select(),
            "tags": SelectMultiple(),
            "show_deadline": CheckboxInput(),
            "visible": CheckboxInput(),
        }


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Category
        fields = ["title", "order", "login_required"]
        labels = {
            "title": _("Category"),
            "order": _("Order"),
            "login_required": _("Visibility"),
        }
        widgets = {
            "title": TextInput(),
            "order": NumberInput(),
            "login_required": Select(
                choices=((False, _("Public")), (True, _("Login required")))
            ),
        }


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ["title"]
        labels = {"title": _("Add a new tag")}
        widgets = {
            "title": TextInput(
                attrs={"class": "form-control", "placeholder": _("Add tag")}
            )
        }


class MailConfigurationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailConfigurationForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if not visible.name == "use_tls":
                visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = MailConfiguration
        fields = ["host", "port", "username", "password", "use_tls"]
        labels = {
            "host": _("Host"),
            "port": _("Port"),
            "username": _("Username (email)"),
            "password": _("Password"),
            "use_tls": _("Use TLS Encryption"),
        }
        widgets = {
            "host": TextInput(),
            "port": NumberInput(),
            "username": TextInput(),
            "password": PasswordInput(),
            "use_tls": CheckboxInput(),
        }


class SendEmailForm(Form):
    def __init__(self, *args, **kwargs):
        super(SendEmailForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    subject = CharField(widget=TextInput(), label=_("Title"))
    to = CharField(widget=TextInput(), label=_("Recipients (separated by comma)"))
