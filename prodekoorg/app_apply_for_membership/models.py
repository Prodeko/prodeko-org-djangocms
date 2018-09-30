import datetime

from django.conf import settings
from django.contrib import messages
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
#from auth_prodeko.models import User


class PendingUser(models.Model):
    """ PendingUser model

    User that has applied to Prodeko through the website
    """

    MEMBERSHIP_TYPE_CHOICES = (
        ('1', _('True member')),
        ('2', _('Alumn')),
        ('3', _('External member')),
    )

    AYY_MEMBER_CHOICES = (
        ('Y', _('Yes')),
        ('N', _('No')),
    )

    YEAR_CHOICES = []
    for r in reversed(range(1966, (datetime.datetime.now().year + 1))):
        YEAR_CHOICES.append((r, r))

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name=_('First name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'))
    hometown = models.CharField(max_length=50, verbose_name=_('Hometown'))
    field_of_study = models.CharField(max_length=50, verbose_name=_('Field of study'))
    email = models.EmailField(verbose_name=_('Email'))
    start_year = models.IntegerField(verbose_name=_('Year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPE_CHOICES, verbose_name=_('Membership type'))
    additional_info = models.TextField(blank=True, verbose_name=_('Why do you want to become a member?'))
    is_ayy_member = models.CharField(max_length=12, choices=AYY_MEMBER_CHOICES, verbose_name=_('Are you an AYY (Aalto University Student Union) member?'))
    receipt = models.FileField(blank=True, null=True, upload_to='jäsenhakemukset/%Y-%m', verbose_name=_('Receipt of the membership payment'),
                               validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])

   # @receiver(post_save, sender=User)
   # def create_user_profile(sender, instance, created, **kwargs):
   #     if created:
   #         PendingUser.objects.create(user=instance)


    def acceptMembership(self, request, account_id, *args, **kwargs):
        #TODO: send email?
        self.user.is_active = True
        self.user.save()
        messages.success(request, 'Membership application accepted.')
        self.delete()

    def rejectMembership(self, request, account_id, *args, **kwargs):
        #TODO: send email?
        messages.success(request, 'Membership application rejected.')
        self.user.delete()
        self.delete()

    def __str__(self):
        first_name = self.first_name
        last_name = self.last_name
        field_of_study = self.field_of_study
        return '{} {} - {}'.format(first_name, last_name, field_of_study)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('membership application')
        verbose_name_plural = _('Membership applications')


