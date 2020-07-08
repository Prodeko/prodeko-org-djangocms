from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def upload_url(instance, filename):
    date = datetime.now()
    yearmonth = date.strftime("%Y-%m")
    return f"kulukorvaukset/{yearmonth}/{uuid4()}/{filename}"


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
        phone_number: Phone number.
        bank_number: Bank account number. Finnish IBAN numbers are 18 chars,
            Saint Lucia is 32 (https://www.iban.com/structure.html).
        bic: Bank identification code. It is 8-11 characters long (https://fi.wikipedia.org/wiki/ISO_9362).
        sum_overall: Total reimbursement claim sum.
        additional_info: Any additional information about the claim.
        status: The status of the reimbursement claim (new, in process or procesed).
        pdf: PDF file representing the reimbursement claim.
    """

    STATUS_CHOICES = (
        ("NEW", _("New")),
        ("IP", _("In process")),
        ("PR", _("Processed")),
    )

    BIC_CHOICES = (
        ("Aktia", "HELSFIHH"),
        ("Danske Bank", "DABAFIHH"),
        ("Danske Bank", "DABAFIHX"),
        ("Handelsbanken", "HANDFIHH"),
        ("Nordea", "NDEAFIHH"),
        ("OmaSp", "OMASP"),
        ("Osuuspankki", "OKOYFIHH"),
        ("POP Pankki", "POPFFI22"),
        ("S-Pankki", "SBANFIHH"),
        ("Säästöpankki", "ITELFIHH"),
        ("Ålandsbanken", "AABAFI22"),
    )

    id = models.AutoField(primary_key=True)
    # on_delete=models.CASCADE means that if a user is deleted
    # all of the associated KulukorvausPerustiedot objects are deleted as well.
    # This in turn cascades into Kulukorvaus objects, they are deleted also.
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    created_by = models.CharField(max_length=50, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone_number = models.CharField(max_length=15, verbose_name=_("Phone number"))
    bank_number = models.CharField(
        max_length=32, verbose_name=_("Account number (IBAN)")
    )
    bic = models.CharField(max_length=11, choices=BIC_CHOICES, verbose_name="BIC")
    sum_overall = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Total reimbursement (in €)")
    )
    additional_info = models.TextField(
        blank=True, verbose_name=_("Additional information")
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, verbose_name=_("Status"), default="NEW"
    )
    pdf = models.FileField(
        blank=True,
        null=True,
        upload_to=upload_url,
        verbose_name="PDF",
        validators=[FileExtensionValidator(["pdf"])],
    )

    def pdf_filename(self):
        created_at = self.kulukorvaus_set.all().first().created_at.date()
        filename = f"{created_at}_kulukorvaus_{self.created_by.replace(' ', '_')}.pdf"
        return filename

    def __str__(self):
        by = self.created_by
        s = self.sum_overall
        return f"{by}, ({s}€)"

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("reimbursement basic information")
        verbose_name_plural = _("Reimbursement basic information")


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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    # on_delete=models.CASCADE means that if a KulukorvausPerustiedot object
    # which is a foreign key of this model is deleted, then this object is deleted also.
    info = models.ForeignKey(
        KulukorvausPerustiedot, models.CASCADE, blank=True, null=True
    )
    target = models.CharField(max_length=50, verbose_name=_("Expense explanation"))
    explanation = models.CharField(
        max_length=100, verbose_name=_("Event / expense target")
    )
    sum_euros = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Sum (in €)")
    )
    additional_info = models.TextField(
        blank=True, verbose_name=_("Additional information")
    )
    receipt = models.FileField(
        upload_to=upload_url,
        verbose_name=_("Receipt"),
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    )

    def __str__(self):
        return f"{self.explanation} ({self.sum_euros}€)"

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("reimbursement")
        verbose_name_plural = _("Reimbursements")
