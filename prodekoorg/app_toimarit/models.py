import os.path

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Jaosto(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class Toimari(models.Model):
    firstname = models.CharField(max_length=30, verbose_name=_('First name'))
    lastname = models.CharField(max_length=30, verbose_name=_('Last name'))
    position = models.CharField(max_length=50, verbose_name=_('Position'))
    section = models.ForeignKey(Jaosto, verbose_name=_('Section'))

    @property
    def name(self):
        return '%s %s' % (self.firstname, self.lastname)

    def photoExists(self):
        return os.path.isfile("prodekoorg/app/toimarit/static/images/toimari_photos/" + self.firstname + "_" + self.lastname + ".jpg")

    def __str__(self):
        return self.name + ", " + self.position

    class Meta:
        verbose_name = _('guild official')
        verbose_name_plural = _('guild officials')


class HallituksenJasen(models.Model):

    firstname = models.CharField(max_length=30, verbose_name=_('First name'))
    lastname = models.CharField(max_length=30, verbose_name=_('Last name'))
    position = models.CharField(max_length=50, verbose_name=_('Position'))
    section = models.ForeignKey(Jaosto, blank=True, null=True, verbose_name=_('Section'))
    position_eng = models.CharField(max_length=60, verbose_name=_('Position (English)'))
    mobilephone = models.CharField(max_length=20, verbose_name=_('Mobile phone'))
    email = models.CharField(max_length=30, verbose_name=_('Email'))
    telegram = models.CharField(max_length=20, verbose_name=_('Telegram'), blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name=_('Description'), blank=True, null=True)

    @property
    def name(self):
        return '%s %s' % (self.firstname, self.lastname)

    def photoExists(self):
        return os.path.isfile("prodekoorg/app_toimarit/static/images/hallitus_photos/" + self.firstname + "_" + self.lastname + ".jpg")

    def __str__(self):
        return self.name + ", " + self.position

    class Meta:
        verbose_name = _('board member')
        verbose_name_plural = _('board members')
