import datetime

from django.conf import settings
from django.contrib import messages
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives


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
    receipt = models.FileField(blank=True, null=True, upload_to='jasenhakemukset/%Y-%m', verbose_name=_('Receipt of the membership payment'),
                               validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])

   # @receiver(post_save, sender=User)
   # def create_user_profile(sender, instance, created, **kwargs):
   #     if created:
   #         PendingUser.objects.create(user=instance)


    def acceptMembership(self, request, account_id, *args, **kwargs):
        password = get_random_string(length=16)
        self.user.set_password(password)
        self.send_accept_email(self.user, password)
        self.user.is_active = True
        self.user.save()
        messages.success(request, _('Membership application accepted.'))
        self.delete()

    def rejectMembership(self, request, account_id, *args, **kwargs):
        self.send_reject_email(self.user)
        messages.success(request, _('Membership application rejected.'))
        self.user.delete()
        self.delete()



    def send_accept_email(self, user, password):
        # inform user about accepted application
        subject = 'Your Application to Prodeko has been accepted'
        text_content = 'Hello, {} {}!' \
            'Your application to join Prodeko has been accepted. You can now login to https://prodeko.org/ using the following credentials:\n' \
            'Email: {}\n Password: {}\n\nPlease change your password after logging in.'.format(user.first_name, user.last_name, user.email, password)
        html_content = '<p>Hello, {} {}!' \
            'Your application to join Prodeko has been accepted. You can now login to https://prodeko.org/ using the following credentials:\n' \
            '<strong>Email:</string> {}\n <strong>Password:</strong> {}\n\nPlease change your password after logging in.</p>'.format(user.first_name, user.last_name, user.email, password)
        email_to = user.email
        from_email = 'no-reply@prodeko.org'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def send_reject_email(self, user):
        # inform user about rejected application
        subject = 'Your Application to Prodeko has been rejected'
        text_content = 'Hello, {} {}!' \
            'Your application to join Prodeko has been rejected.'.format(user.first_name, user.last_name)
        html_content = '<p>Hello, {} {}!' \
            'Your application to join Prodeko has been rejected.'.format(user.first_name, user.last_name)
        email_to = user.email
        from_email = 'no-reply@prodeko.org'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def __str__(self):
        first_name = self.first_name
        last_name = self.last_name
        field_of_study = self.field_of_study
        return '{} {} - {}'.format(first_name, last_name, field_of_study)

    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('membership application')
        verbose_name_plural = _('Membership applications')
