import datetime

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _ 


class PendingUser(models.Model):
    """ PendingUser model

    User that has applied to Prodeko through the website
    """

    MEMBERSHIP_TYPE_CHOICES = (
        ('Varsinainen', 'Varsinainen jäsen'),
        ('Alumni', 'Alumni'),
        ('Ulkojäsen', 'Ulkojäsen'),
    )

    AYY_MEMBER_CHOICES = (
        ('Kyllä', 'Kyllä'),
        ('Ei', 'Ei'),
    )

    YEAR_CHOICES = []
    for r in range(1966, (datetime.datetime.now().year)):
        YEAR_CHOICES.append((r, r))

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Nimi')
    hometown = models.CharField(max_length=50, verbose_name='Kotipaikka')
    field_of_study = models.CharField(max_length=50, verbose_name='Opiskeluala')
    email = models.EmailField(verbose_name='Sähköposti')
    start_year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPE_CHOICES, verbose_name='Jäsentyyppi')
    additional_info = models.TextField(blank=True, verbose_name='Miksi haluat jäseneksi?')
    is_ayy_member = models.CharField(max_length=12, choices=AYY_MEMBER_CHOICES, verbose_name='Oletko AYY:n jäsen?')
    receipt = models.FileField(blank=True, null=True, upload_to='jäsenhakemukset/%Y-%m', verbose_name='Kuitti jäsenmaksusta',
                               validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])

    def __str__(self):
        name = self.name
        field_of_study = self.field_of_study
        return '{} - {}'.format(name, field_of_study)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('jäsenhakemus')
        verbose_name_plural = _('Jäsenhakemukset')