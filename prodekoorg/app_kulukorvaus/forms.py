from django.forms import ModelForm, RadioSelect, Textarea
from django.utils.translation import ugettext_lazy as _

from .models import Kulukorvaus, KulukorvausPerustiedot


class KulukorvausPerustiedotForm(ModelForm):
    """KulukorvausPerustiedotForm class extending Django's ModelForm.

    Maps KulukorvausPerustiedot model's fields to HTML form <input> elements.
    """

    def __init__(self, *args, **kwargs):
        """Overrides the ModelForm __init__ method.

        This way we can attach widgets and bootstrap classess
        to certain form fields to make them look better in the UI.
        """

        # Call ModelForm __init__ method.
        super(KulukorvausPerustiedotForm, self).__init__(*args, **kwargs)

        if "position_in_guild" in self.fields:
            # Attach a RadioSelect widget to the position_in_guild for field
            self.fields["position_in_guild"].widget = RadioSelect(
                choices=KulukorvausPerustiedot.POSITION_CHOICES
            )
        for visible in self.visible_fields():
            if not visible.name == "position_in_guild":
                # 'form-control' is a bootstrap class used to style
                # form fields appropriately.
                visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = KulukorvausPerustiedot
        exclude = [
            "created_by_user"
        ]  # Don't include 'created_by_user' in the form. It is inferred from the HttpRequest.
        localized_fields = (
            "sum_overall",
        )  # Use ',' as a decimal separator for Finnish and '.' in English
        widgets = {
            "additional_info": Textarea(
                attrs={"rows": 1, "cols": 1}
            )  # Override Textarea default height
        }


class KulukorvausForm(ModelForm):
    """KulukorvausForm class extending Django's ModelForm.

    Maps Kulukorvaus model's fields to HTML form <input> elements.
    """

    def __init__(self, *args, **kwargs):
        super(KulukorvausForm, self).__init__(*args, **kwargs)
        # The KulukorvausForm can't be empty.
        self.empty_permitted = False

        for visible in self.visible_fields():
            # 'form-control' is a bootstrap class used to style
            # form fields appropriately.
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Kulukorvaus
        fields = "__all__"  # Use all model fields in form creation.
        localized_fields = (
            "sum_euros",
        )  # Use ',' as a decimal separator for Finnish and '.' in English
        widgets = {
            "additional_info": Textarea(
                attrs={"rows": 1, "cols": 1}
            )  # Override Textarea default height
        }
        help_texts = {
            "target": _(
                'e.g. "Food expenses", "Coffee to the guildroom" or "Mileage allowance"'
            ),
            "explanation": _(
                'e.g. "Fall sitz", "Freshmen meetup" or "Guildroom renovations"'
            ),
        }
