import os
from ckeditor.fields import RichTextField
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Virka(models.Model):
    """ Position in the elections.
    """

    is_hallitus = models.BooleanField(default=False, verbose_name='Hallitus')
    section = models.CharField(max_length=50, verbose_name='Jaos', blank=True)
    name = models.CharField(max_length=50, verbose_name='Virka')

    def __str__(self):
        nimi = self.name
        return '{}'.format(nimi)

    def get_ehdokkaat(self):
        print(self.ehdokkaat)
        print(self.name)
        return self.ehdokkaat

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('virka')
        verbose_name_plural = _('Virat')


class Ehdokas(models.Model):
    """ Applicant in the elections.
    """

    id = models.AutoField(primary_key=True)
    auth_prodeko_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name='Nimi')
    introduction = RichTextField(config_name='vaalit_ckeditor')
    virka = models.ManyToManyField(Virka, related_name='ehdokkaat')
    pic = models.ImageField(blank=True, verbose_name='Kuva')

    def __str__(self):
        v = self.virka
        nimi = self.name
        return '{}, {}'.format(v, nimi)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('ehdokas')
        verbose_name_plural = _('Ehdokkaat')


class Kysymys(models.Model):
    """ Question assigned to a specific candidate (Ehdokas).
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Luotu')
    to_applicant = models.ForeignKey(Virka, on_delete=models.CASCADE, related_name='kysymykset')
    question = models.TextField(blank=True, verbose_name='Kysymys')

    def __str__(self):
        to_applicant = self.to_applicant
        return '{}'.format(to_applicant)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('kysymys')
        verbose_name_plural = _('Kysymykset')
