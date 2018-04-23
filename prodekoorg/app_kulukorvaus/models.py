from datetime import datetime

from django.conf import settings
from django.db import models
from django.forms import ModelForm, ChoiceField, RadioSelect
from django.utils import timezone
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _


class Kulukorvaus(models.Model):
    """ Kulukorvaus model

    The model is used for electric reimbursement.
    """

    POSITION_CHOICES = (
        ('Hallitus', 'Hallitus'),
        ('Toimihenkilö', 'Toimihenkilö'),
    )

    BIC_CHOICES = (
        ('OP Ryhmä', 'OKOYFIHH'),
        ('Nordea', 'NDEAFIHH'),
        ('S Pankki', 'SBANFIHH'),
        ('Danske Bank', 'DABAFIHH'),
        ('Handelsbanken', 'HANDFIHH'),
    )

    def validate_iban(self):
        pass

    id = models.AutoField(primary_key=True)
    # Used to track which User created the kulukorvaus
    created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Luotu')
    created_by = models.CharField(max_length=50, verbose_name='Nimi')
    email = models.EmailField(unique=True, verbose_name='Sähköposti')
    position_in_guild = models.CharField(max_length=12, choices=POSITION_CHOICES, verbose_name='Asema killassa')
    phone_number = models.CharField(max_length=15, verbose_name='Puhelinnumero')
    # Finnish IBAN numbers are 18 chars, Saint Lucia is 32
    # Source: https://www.iban.com/structure.html
    bank_number = models.CharField(max_length=32, verbose_name='Tilinumero (IBAN)')
    # BIC is 8-11 characters long
    bic = models.CharField(max_length=11, choices=BIC_CHOICES, verbose_name='BIC')
    target = models.CharField(max_length=50, verbose_name='Kulun selite')
    explanation = models.TextField(verbose_name='Tapahtuma / kulun kohde')
    sum_euros = models.PositiveIntegerField(verbose_name='Summa (euroa)')
    additional_info = models.TextField(blank=True, verbose_name='Lisätietoja, kulujen perusteita')
    receipt = models.FileField(upload_to='kulukorvaukset', verbose_name='Kuitti')

    def __str__(self):
        return str(self.created_at) + ';' + self.created_by

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('kulukorvaus')
        verbose_name_plural = _('Kulukorvaukset')

    def get_absolute_url(self):
        return "kulukorvaukset/%s/%s" % (self.created_at.year, self.id)


class KulukorvausForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(KulukorvausForm, self).__init__(*args, **kwargs)
        self.fields['position_in_guild'].widget = RadioSelect(
                   choices=Kulukorvaus.POSITION_CHOICES)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Kulukorvaus
        exclude = ['created_by_user']
