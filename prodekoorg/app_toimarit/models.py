import os.path

from django.db import models
from django.utils.html import *
from django.utils.translation import ugettext_lazy as _


class Jaosto(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class Toimari(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    position = models.CharField(max_length=50)
    section = models.ForeignKey(Jaosto)

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

    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    position = models.CharField(max_length=50)
    section = models.ForeignKey(Jaosto, blank=True, null=True)
    position_eng = models.CharField(max_length=60)
    mobilephone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)

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
