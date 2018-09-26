import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Kuitin on oltava .png, .jpg tai .jpeg muodossa.')


def validate_iban(self):
    pass


class KulukorvausPerustiedot(models.Model):
    """ Kulukorvaus perustiedot model

    Basic information about the person
    """

    POSITION_CHOICES = (
        ('Hallitus', 'Hallitus'),
        ('Toimihenkilö', 'Toimihenkilö'),
    )

    BIC_CHOICES = (
        ('OKOYFIHH', 'OKOYFIHH'),
        ('NDEAFIHH', 'NDEAFIHH'),
        ('SBANFIHH', 'SBANFIHH'),
        ('DABAFIHH', 'DABAFIHH'),
        ('HANDFIHH', 'HANDFIHH'),
    )

    id = models.AutoField(primary_key=True)
    # Used to track which User created the kulukorvaus
    created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.CharField(max_length=50, verbose_name=_('Name'))
    email = models.EmailField(verbose_name='Sähköposti')
    position_in_guild = models.CharField(max_length=12, choices=POSITION_CHOICES, verbose_name=_('Position in guild'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone number'))
    # Finnish IBAN numbers are 18 chars, Saint Lucia is 32
    # Source: https://www.iban.com/structure.html
    bank_number = models.CharField(max_length=32, verbose_name=_('Account number (IBAN)'))
    # BIC is 8-11 characters long
    bic = models.CharField(max_length=11, choices=BIC_CHOICES, verbose_name='BIC')
    sum_overall = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Total reimbursement (in €)'))
    additional_info = models.TextField(blank=True, verbose_name=_('Additional information'))
    pdf = models.FileField(blank=True, null=True, upload_to='kulukorvaukset/%Y-%m', verbose_name='PDF',
                           validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        position = self.position_in_guild
        by = self.created_by
        s = self.sum_overall
        return '{}, {}, {}€'.format(position, by, s)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('reimbursement basic information')
        verbose_name_plural = _('Reimbursement basic information')


class Kulukorvaus(models.Model):
    """ Kulukorvaus model

    Basic information about the person
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    info = models.ForeignKey(KulukorvausPerustiedot, models.SET_NULL, blank=True, null=True)
    target = models.CharField(max_length=50, verbose_name=_('Expense explanation'))
    explanation = models.CharField(max_length=100, verbose_name=_('Event / expense target'))
    sum_euros = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Sum (in €)'))
    additional_info = models.TextField(blank=True, verbose_name=_('Additional info'))
    receipt = models.FileField(upload_to='kulukorvaukset/%Y-%m', verbose_name=_('Receipt'),
                               validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    def __str__(self):
        time = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        explanation = self.explanation
        return '{}-{}'.format(time, explanation)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('reimbursement')
        verbose_name_plural = _('Reimbursements')

    def get_absolute_url(self):
        return "kulukorvaukset/{}/{}".format(self.created_at.year, self.id)
