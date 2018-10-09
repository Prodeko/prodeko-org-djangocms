from django.forms import ModelForm, RadioSelect, Textarea
from django.utils.translation import ugettext_lazy as _

from .models import Kulukorvaus, KulukorvausPerustiedot


class KulukorvausPerustiedotForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(KulukorvausPerustiedotForm, self).__init__(*args, **kwargs)

        if 'position_in_guild' in self.fields:
            self.fields['position_in_guild'].widget = RadioSelect(
                choices=KulukorvausPerustiedot.POSITION_CHOICES)
        for visible in self.visible_fields():
            if not visible.name == 'position_in_guild':
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = KulukorvausPerustiedot
        exclude = ['created_by_user']
        localized_fields = ('sum_overall',)
        # Override Textarea default height
        widgets = {
            'additional_info': Textarea(attrs={'rows': 1, 'cols': 1}),
        }


class KulukorvausForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(KulukorvausForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Kulukorvaus
        fields = '__all__'
        localized_fields = ('sum_euros',)
        # Override Textarea default height
        widgets = {
            'additional_info': Textarea(attrs={'rows': 1, 'cols': 1}),
        }
        # 'esim. "Ruokakulut", "Kahvia kiltikselle" tai "Kilometrikorvaus"'
        # 'esim. "Syyssitsit", "Fuksiryhmätapaaminen" tai "Kiltahuoneen uudistaminen"'
        help_texts = {
            'target': _('e.g. "Food expenses", "Coffee to the guildroom" or "Mileage allowance"'),
            'explanation': _('e.g. "Fall sitz", "Freshmen meetup" or "Guildroom renovations"'),
        }
