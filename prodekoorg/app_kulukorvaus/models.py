from time import localtime, strftime

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class KulukorvausPerustiedot(models.Model):
    """Basic information about the reimbursement claim as a whole.

    Kulukorvaus perustiedot model contains basic information
    about the reimbursement claim as well as acts as a Foreign key to
    bind togethen Kulukorvaus objects (defined below in another class)
    under one KulukorvausPerustiedot object.

    Attributes:
        id: Primary key.
        created_by_user: Tracks which User created the reimbursement.
        created_by: Name of the person who created the claim.
        email: Email address.
        position_in_guild: Position in the guild, either 'Hallitus' or 'Toimihenkilö'.
        phone_number: Phone number.
        bank_number: Bank account number. Finnish IBAN numbers are 18 chars,
            Saint Lucia is 32 (https://www.iban.com/structure.html).
        bic: Bank identification code. It is 8-11 characters long (https://fi.wikipedia.org/wiki/ISO_9362).
        sum_overall: Total reimbursement claim sum.
        additional_info: Any additional information about the claim.
        pdf: PDF file representing the reimbursement claim.
    """

    POSITION_CHOICES = (
        ('H', _('Board')),
        ('T', _('Guild official')),
    )

    BIC_CHOICES = (
        ('OP', 'OKOYFIHH'),
        ('NORDEA', 'NDEAFIHH'),
        ('SPANKKI', 'SBANFIHH'),
        ('DANSKE', 'DABAFIHH'),
        ('HANDELS', 'HANDFIHH'),
    )

    id = models.AutoField(primary_key=True)
    # on_delete=models.CASCADE means that if a user is deleted
    # all of the associated KulukorvausPerustiedot objects are deleted as well.
    # This in turn cascades into Kulukorvaus objects, they are deleted also.
    created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.CharField(max_length=50, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    position_in_guild = models.CharField(max_length=12, choices=POSITION_CHOICES, verbose_name=_('Position in guild'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone number'))
    bank_number = models.CharField(max_length=32, verbose_name=_('Account number (IBAN)'))
    bic = models.CharField(max_length=11, choices=BIC_CHOICES, verbose_name='BIC')
    sum_overall = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Total reimbursement (in €)'))
    additional_info = models.TextField(blank=True, verbose_name=_('Additional information'))
    pdf = models.FileField(blank=True, null=True, upload_to='kulukorvaukset/%Y-%m', verbose_name='PDF',
                           validators=[FileExtensionValidator(['pdf'])])

    def pdf_filename(self):
        created_at = self.kulukorvaus_set.all().first().created_at.date()
        filename = '{}_kulukorvaus_{}.pdf'.format(created_at, self.created_by.replace(" ", "_"))
        return filename

    def __str__(self):
        position_in_guild = self.position_in_guild
        by = self.created_by
        s = self.sum_overall
        return '{} - {}, ({}€)'.format(position_in_guild, by, s)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('reimbursement basic information')
        verbose_name_plural = _('Reimbursement basic information')


class Kulukorvaus(models.Model):
    """Represents individual reimbursement claims from for example separate events.

    Attributes:
        created_at: Timestamp of object creation.
        info: Foreign key pointing to a KulukorvausPerustiedot model.
        target: Event / expense target
        explanation: Expense explanation.
        sum_euros: Expense sum in euros.
        additional_info: Any additional information about the claim.
        receipt: Receipt of the purchase, must be jpg, png or jpeg.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    # on_delete=models.CASCADE means that if a KulukorvausPerustiedot object
    # which is a foreign key of this model is deleted, then this object is deleted also.
    info = models.ForeignKey(KulukorvausPerustiedot, models.CASCADE, blank=True, null=True)
    target = models.CharField(max_length=50, verbose_name=_('Expense explanation'))
    explanation = models.CharField(max_length=100, verbose_name=_('Event / expense target'))
    sum_euros = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Sum (in €)'))
    additional_info = models.TextField(blank=True, verbose_name=_('Additional information'))
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
