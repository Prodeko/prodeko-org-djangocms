from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def content_directory(instance, filename):
    """ Specify upload directory at runtime.

    Uploads the model instance to a directory that
    gets secified using the model itself.

    For example, say we upload 'pöytäkirja2018-02.pdf'
    to the server. We would like to have a folder
    /dokumentit/2018/2/pöytäkirja2018-2.pdf to keep
    things organized. The '/2' folder is needed since
    proceedings documents regularly have attachments.
    """
    return '/'.join(['dokumentit', str(instance.date.year), str(instance.number), filename])


class Dokumentti(models.Model):
    """ Document models

    The model is used for proceedings (pöytäkirja) uploads.
    """

    name = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField()
    date = models.DateField()
    doc_file = models.FileField(upload_to=content_directory)

    def __str__(self):
        return self.name

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('pöytäkirja')
        verbose_name_plural = _('Pöytäkirjat')
        ordering = ['-date', '-number']

    def get_absolute_url(self):
        return "%s" % (self.doc_file.url)
