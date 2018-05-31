from django import forms
from django.core.files import File
from django.forms import ModelForm, Textarea
from PIL import Image
from .models import Ehdokas


class EhdokasForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EhdokasForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Ehdokas
        fields = ['name', 'introduction', 'pic']
