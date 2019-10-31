import datetime

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


class PendingUser(models.Model):
    """Basic information about the reimbursement claim as a whole.

    The PendingUser model contains information about people who
    have applied to become Prodeko members. 

    Attributes:
        id: Primary key.
        user: Tracks which User created the membership application.
        first_name: First name of the applicant.
        last_name: Last name of the applicant.
        hometown: Hometown of the applicant.
        field_of_study: Field of study of the applicant.
        email: Email address of the applicant.
        start_year: The year in which the applicant started their studies.
        language: Preferred language - either Finnish or English
        membership_type: Membership type.
        additional_info: Any additional information about the membership application.
        is_ayy_member: Boolen indicating whether the person is part of AYY student union or not.
        receipt: Receipt for the membership payment.
        has_accepted_policies: Designates whether the user has accepted Prodeko's privacy policy.
    """

    TRUE_MEMBER = "TR"
    ALUMN_MEMBER = "AL"
    EXTERNAL_MEMBER = "EX"

    MEMBERSHIP_TYPE_CHOICES = (
        (TRUE_MEMBER, _("True member")),
        (ALUMN_MEMBER, _("Alumn")),
        (EXTERNAL_MEMBER, _("External member")),
    )

    AYY_MEMBER_CHOICES = (("Y", _("Yes")), ("N", _("No")))

    LANGUAGE_CHOICES = (("FI", _("Finnish")), ("EN", _("Other (English)")))

    YEAR_CHOICES = []
    for r in reversed(range(1966, (datetime.datetime.now().year + 1))):
        YEAR_CHOICES.append((r, r))

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    first_name = models.CharField(max_length=50, verbose_name=_("First name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last name"))
    hometown = models.CharField(max_length=50, verbose_name=_("Hometown"))
    field_of_study = models.CharField(max_length=50, verbose_name=_("Field of study"))
    email = models.EmailField(verbose_name=_("Email"))
    start_year = models.IntegerField(
        verbose_name=_("Year"),
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
    )
    language = models.CharField(
        max_length=50, choices=LANGUAGE_CHOICES, verbose_name=_("Preferred language")
    )
    membership_type = models.CharField(
        max_length=2, choices=MEMBERSHIP_TYPE_CHOICES, verbose_name=_("Membership type")
    )
    additional_info = models.TextField(
        blank=True, verbose_name=_("Why do you want to become a member?")
    )
    is_ayy_member = models.CharField(
        max_length=1,
        choices=AYY_MEMBER_CHOICES,
        verbose_name=_("Are you an AYY (Aalto University Student Union) member?"),
    )
    receipt = models.FileField(
        upload_to="jasenhakemukset/%Y-%m",
        verbose_name=_("Receipt of the membership payment"),
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
    )
    has_accepted_policies = models.BooleanField(
        default=False, verbose_name=_("I accept Prodeko's privacy policy")
    )

    def accept_membership(self, request, account_id, *args, **kwargs):
        password = get_random_string(length=16)
        self.user.set_password(password)
        self.send_accept_email(self.user, password)
        self.user.is_active = True
        self.user.save()
        messages.success(request, _("Membership application accepted."))
        self.delete()

    def reject_membership(self, request, account_id, *args, **kwargs):
        self.send_reject_email(self.user)
        messages.success(request, _("Membership application rejected."))
        self.user.delete()
        self.delete()

    def send_accept_email(self, user, password):
        # Inform user about accepted application
        subject = "Your application to Prodeko has been accepted"
        template = "accept_mail_en" if self.language == "EN" else "accept_mail_fi"
        text_content = render_to_string(
            f"{template}.txt", {"user": user, "password": password}
        )
        html_content = render_to_string(
            f"{template}.html", {"user": user, "password": password}
        )
        email_to = user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def send_reject_email(self, user):
        # Inform user about rejected application
        subject = "Your application to Prodeko has been rejected"
        template = "reject_mail_en" if self.language == "EN" else "reject_mail_fi"
        text_content = render_to_string(f"{template}.txt", {"user": user})
        html_content = render_to_string(f"{template}.html", {"user": user})
        email_to = user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def __str__(self):
        first_name = self.first_name
        last_name = self.last_name
        field_of_study = self.field_of_study
        return f"{first_name} {last_name} - {field_of_study}"

    def name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("membership application")
        verbose_name_plural = _("Membership applications")
