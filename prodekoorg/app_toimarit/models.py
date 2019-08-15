import os.path

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
        return "%s %s" % (self.firstname, self.lastname)

    def photoExists(self):
        return os.path.isfile(
            "prodekoorg/app_toimarit/static/images/toimari_photos/"
            + self.firstname
            + "_"
            + self.lastname
            + ".jpg"
        )

    def photourl(self):
        if settings.DEBUG:
            if os.path.isfile("prodekoorg/app_toimarit/static/images/toimari_photos/{}_{}.jpg".format(self.firstname, self.lastname)):
                return "%s_%s.jpg" % (self.firstname, self.lastname)
            else:
                return 'placeholder.jpg'
        else:
            if os.path.isfile(settings.STATIC_ROOT + "/images/toimari_photos/{}_{}.jpg".format(self.firstname, self.lastname)):
                return "%s_%s.jpg" % (self.firstname, self.lastname)
            else:
                return 'placeholder.jpg'

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
        return "%s %s" % (self.firstname, self.lastname)

    def photoExists(self):
        return os.path.isfile(
            "prodekoorg/app_toimarit/static/images/hallitus_photos/{}_{}.jpg".format(
                self.firstname, self.lastname
            )
        )

    def photourl(self):
        if settings.DEBUG:
            if os.path.isfile("prodekoorg/app_toimarit/static/images/hallitus_photos/{}_{}.jpg".format(self.firstname, self.lastname)):
                return "%s_%s.jpg" % (self.firstname, self.lastname)
            else:
                return 'placeholder.jpg'
        else:
            if os.path.isfile(settings.STATIC_ROOT + "/images/hallitus_photos/{}_{}.jpg".format(self.firstname, self.lastname)):
                return "%s_%s.jpg" % (self.firstname, self.lastname)
            else:
                return 'placeholder.jpg'

    def __str__(self):
        return f"{self.name}, {self.position}"

    class Meta:
        verbose_name = _("board member")
        verbose_name_plural = _("board members")