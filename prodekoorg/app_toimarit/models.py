import os.path
import unidecode

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


def remove_äö(input_str):
    return unidecode.unidecode(input_str)


def get_photo_url(board_or_official, object):
    if settings.DEBUG:
        if os.path.isfile(
            remove_äö(
                f"prodekoorg/app_toimarit/static/images/{board_or_official}/{object.firstname}_{object.lastname}.jpg"
            )
        ):
            return remove_äö(f"{object.firstname}_{object.lastname}.jpg")
        else:
            return "placeholder.jpg"
    else:
        if os.path.isfile(
            remove_äö(
                f"{settings.STATIC_ROOT}/images/{board_or_official}/{object.firstname}_{object.lastname}.jpg"
            )
        ):
            return remove_äö(f"{object.firstname}_{object.lastname}.jpg")
        else:
            return "placeholder.jpg"


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
        Position: Current position as a Guild Official
        Section: The section in which the Guild Official belongs to based on their position
    """

    firstname = models.CharField(max_length=30, verbose_name=_("First name"))
    lastname = models.CharField(max_length=30, verbose_name=_("Last name"))
    position = models.CharField(max_length=50, verbose_name=_("Position"))
    section = models.ForeignKey(
        Jaosto, verbose_name=_("Section"), on_delete=models.CASCADE
    )

    @property
    def name(self):
        return f"{self.firstname} {self.lastname}"

    def photourl(self):
        return get_photo_url("toimari_photos", self)

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
        position: Current position as a Board Member (in Finnish)
        section: The section of responsibility.
          Not currently displayed anywhere, and exists just to make
          the export CSV function simpler.
        position_eng: English version of the Board Member's position
        mobilephone: Mobile phone number of the Board Member
        telegram: Telegram username of the Board Member.
          Not currently displayed anywhere.
        description: A short description of the role.
          Not currenly displayed anywhere.
    """

    firstname = models.CharField(max_length=30, verbose_name=_("First name"))
    lastname = models.CharField(max_length=30, verbose_name=_("Last name"))
    position = models.CharField(max_length=50, verbose_name=_("Position"))
    section = models.ForeignKey(
        Jaosto,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Section"),
    )
    position_eng = models.CharField(max_length=60, verbose_name=_("Position (English)"))
    mobilephone = models.CharField(max_length=20, verbose_name=_("Mobile phone"))
    email = models.CharField(max_length=30, verbose_name=_("Email"))
    telegram = models.CharField(
        max_length=20, verbose_name=_("Telegram"), blank=True, null=True
    )
    description = models.CharField(
        max_length=255, verbose_name=_("Description"), blank=True, null=True
    )

    @property
    def name(self):
        return f"{self.firstname} {self.lastname}"

    def photourl(self):
        return get_photo_url("hallitus_photos", self)

    def __str__(self):
        return f"{self.name}, {self.position}"

    class Meta:
        verbose_name = _("board member")
        verbose_name_plural = _("board members")
