from django.db import models
from django.utils.translation import ugettext_lazy as _


def content_directory(instance, filename):
    """Specify doc_file upload directory at runtime.

    Uploads the model instance to a directory that
    gets specified using information about the model itself

    For example, say we upload 'pöytäkirja2018-02.pdf'
    to the server. We would like to have a folder
    /dokumentit/2018/2/pöytäkirja2018-2.pdf to keep
    things organized. The '/2' folder is needed since
    proceedings documents regularly have attachments.

    Args:
        instance: Dokumentti object instance.
        filename: Filename.

    Returns:
        A string representing the file upload path.
    """

    return '/'.join(['dokumentit', str(instance.date.year), str(instance.number), filename])


class Dokumentti(models.Model):
    """Prodeko board proceedings documents.

    This model is used to represent prodeko board proceedings (pöytäkirja in Finnish)
    documents. The app_poytakirjat app makes it possible to download documents
    straight from Google Drive and into Django as PDF files. This model represents a
    single board proceedings document.

    Attributes:
        gdrive_id: Google Drive id of the related Google Docs document.
        name: Name of the document.
        number: Running number of the document.
        date: Date of the meeting.
        doc_file: Document file as PDF.
    """

    gdrive_id = models.CharField(max_length=99)
    name = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField()
    date = models.DateField()
    doc_file = models.FileField(upload_to=content_directory)

    def __str__(self):
        return self.name

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _('minutes')
        verbose_name_plural = _('Minutes')
        ordering = ['-date', '-number']

    def get_absolute_url(self):
        return "%s" % (self.doc_file.url)
