from django.forms import ModelForm, Select, Textarea
from django.utils.translation import ugettext_lazy as _

from .models import Message


class ContactForm(ModelForm):
    """ContactForm class extending Django's ModelForm.

    Maps Message model's fields to HTML form <input> elements.
    """

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

        if "contact_emails" in self.fields:
            self.fields["contact_emails"].widget = Select(
                choices=[(k, f"{label}") for k, v, label in Message.CONTACT_EMAILS]
            )

        for visible in self.visible_fields():
            if visible.name not in ["has_accepted_policies"]:
                visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Message
        fields = ["email", "contact_emails", "message", "has_accepted_policies"]
        widgets = {"message": Textarea(attrs={"rows": 4, "cols": 1})}
        help_texts = {"email": _("Optional. Fill if you want to be contacted back.")}
