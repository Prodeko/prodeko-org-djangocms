import os.path

from django.db import models
from django.utils.html import *
from django.utils.translation import ugettext_lazy as _


class Jaosto(models.Model):
    nimi = models.CharField(max_length=50)

    def __str__(self):
        return self.nimi

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class Toimari(models.Model):

    # Toimareille ja hallituslaisille
    etunimi = models.CharField(max_length=30)
    sukunimi = models.CharField(max_length=30)
    virka = models.CharField(max_length=50)
    jaosto = models.ForeignKey(Jaosto)

    @property
    def name(self):
        return '%s %s' % (self.etunimi, self.sukunimi)

    def photoExists(self):
        return os.path.isfile("prodekoorg/app/toimarit/static/images/toimari_photos/" + self.etunimi + "_" + self.sukunimi + ".jpg")

    def __str__(self):
        return self.name + ", " + self.virka

    class Meta:
        verbose_name = _('guild official')
        verbose_name_plural = _('guild officials')


class HallituksenJasen(models.Model):

    etunimi = models.CharField(max_length=30)
    sukunimi = models.CharField(max_length=30)
    virka = models.CharField(max_length=50)
    jaosto = models.ForeignKey(Jaosto)
    virka_eng = models.CharField(max_length=60)
    puhelin = models.CharField(max_length=20)
    sahkoposti = models.CharField(max_length=30)

    @property
    def name(self):
        return '%s %s' % (self.etunimi, self.sukunimi)

    def photoExists(self):
        return os.path.isfile("prodekoorg/app_toimarit/static/images/hallitus_photos/" + self.etunimi + "_" + self.sukunimi + ".jpg")

    def __str__(self):
        return self.name + ", " + self.virka

    class Meta:
        verbose_name = _('board member')
        verbose_name_plural = _('board members')
