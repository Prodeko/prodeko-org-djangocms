from django.forms import ModelForm

from .models import Ehdokas, Kysymys, Vastaus


class EhdokasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EhdokasForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Ehdokas
        fields = ["name", "introduction", "pic"]


class KysymysForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(KysymysForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Kysymys
        fields = ["question"]


class VastausForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VastausForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Vastaus
        fields = ["answer"]
