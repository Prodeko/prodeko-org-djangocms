from django.db import models
from django.utils.html import *
import os.path


class Toimari(models.Model):

    # Toimareille ja hallituslaisille
    etunimi = models.CharField(max_length=30)
    sukunimi = models.CharField(max_length=30)
    virka = models.CharField(max_length=50)
    jaosto = models.CharField(max_length=100)

    @property
    def name(self):
        return '%s %s' % (self.etunimi, self.sukunimi)

    def photoExists(self):
        return os.path.isfile("prodekoorg/static/images/toimari_photos/" + self.etunimi + "_" + self.sukunimi + ".jpg")

    def __str__(self):
        return self.name + ", " + self.virka

    class Meta:
        verbose_name_plural = "toimarit"

class HallituksenJasen(models.Model):

    etunimi = models.CharField(max_length=30)
    sukunimi = models.CharField(max_length=30)
    virka = models.CharField(max_length=50)
    jaosto = models.CharField(max_length=100)
    virka_eng = models.CharField(max_length=60)
    puhelin = models.CharField(max_length=20)
    sahkoposti = models.CharField(max_length=30)

    @property
    def name(self):
        return '%s %s' % (self.etunimi, self.sukunimi)

    def photoExists(self):
        return os.path.isfile("prodekoorg/static/images/hallitus_photos/" + self.etunimi + "_" + self.sukunimi + ".jpg")

    def __str__(self):
        return self.name + ", " + self.virka

    class Meta:
        verbose_name_plural = "hallituksen jäsenet"
