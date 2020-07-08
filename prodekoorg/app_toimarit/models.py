from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField


def default_year():
    return timezone.now().date().year


class Jaosto(models.Model):
    """Prodeko board proceedings documents.

    This model represents a section in Prodeko's organization.

    Attributes:
        name: Name of the section
    """

    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")


class Toimari(models.Model):
    """This model represents a Guild Official in Prodeko.

    Attributes:
        firstname: First name of the Guild Official
        lastname: Last name of the Guild Official
        position: Current position as a Guild Official
        section: The section in which the Guild Official belongs to based on their position
        photo: Toimari photo
    """

    firstname = models.CharField(max_length=30, verbose_name=_("First name"))
    lastname = models.CharField(max_length=30, verbose_name=_("Last name"))
    position = models.CharField(max_length=50, verbose_name=_("Position"))
    section = models.ForeignKey(
        Jaosto, verbose_name=_("Section"), on_delete=models.CASCADE
    )
    photo = FilerImageField(
        on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Photo")
    )
    year = models.IntegerField(default=default_year, verbose_name=_("Year"))

    @property
    def name(self):
        return f"{self.firstname} {self.lastname}"

    def __str__(self):
        return f"{self.name}, {self.position}"

    class Meta:
        verbose_name = _("guild official")
        verbose_name_plural = _("guild officials")


class HallituksenJasen(models.Model):
    """This model represents a Board Member in Prodeko.

    Attributes:
        firstname: First name of the Board Member
        lastname: Last name of the Board Member
        position_fi: Current position as a Board Member (in Finnish)
        position_en: English version of the Board Member's position
        mobilephone: Mobile phone number of the Board Member
        telegram: Telegram username of the Board Member.
          Not currently displayed anywhere.
        photo: HallituksenJasen photo
    """

    firstname = models.CharField(max_length=30, verbose_name=_("First name"))
    lastname = models.CharField(max_length=30, verbose_name=_("Last name"))
    position_fi = models.CharField(max_length=50, verbose_name=_("Position"))
    position_en = models.CharField(max_length=60, verbose_name=_("Position (English)"))
    mobilephone = models.CharField(
        max_length=20, verbose_name=_("Mobile phone"), blank=True, null=True
    )
    email = models.CharField(
        max_length=30, verbose_name=_("Email"), blank=True, null=True
    )
    telegram = models.CharField(
        max_length=20, verbose_name=_("Telegram"), blank=True, null=True
    )
    photo = FilerImageField(
        on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Photo")
    )
    year = models.IntegerField(default=default_year, verbose_name=_("Year"))

    @property
    def name(self):
        return f"{self.firstname} {self.lastname}"

    def __str__(self):
        return f"{self.name}, {self.position_fi}"

    class Meta:
        verbose_name = _("board member")
        verbose_name_plural = _("board members")
