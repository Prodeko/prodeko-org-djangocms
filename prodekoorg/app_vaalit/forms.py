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
        fields = ['name', 'introduction']


class PhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Ehdokas
        fields = ['pic', 'x', 'y', 'width', 'height']

    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = photo.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo
