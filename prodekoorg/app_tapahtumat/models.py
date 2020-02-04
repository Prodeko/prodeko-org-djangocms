from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4


def content_directory(instance, filename):
    """Specify doc_file upload directory at runtime.

    Uploads the model instance to a directory that
    gets specified using information about the model itself

    For example, say we upload 'pöytäkirja2018-02.pdf'
    to the server. We would like to have a folder
    /dokumentit/2018/2/pöytäkirja2018-2.pdf to keep
    things organized. The '/2' folder is needed since
    proceedings documents regularly have attachments.

    A unique identifier is added to the path to prevent
    public access to the files.

    Args:
        instance: Tapahtuma object instance.
        filename: Filename.

    Returns:
        A string representing the file upload path.
    """

    return "/".join(
        [
            "dokumentit",
            str(instance.date.year),
            str(instance.number),
            str(uuid4()),
            filename,
        ]
    )


class Tapahtuma(models.Model):
    """Prodeko board proceedings documents.

    This model is used to represent prodeko board proceedings (pöytäkirja in Finnish)
    documents. The app_tapahtumat app makes it possible to download documents
    straight from Google Drive and into Django as PDF files. This model represents a
    single board proceedings document.

    Attributes:
        gdrive_id: Google Drive id of the related Google Docs document.
        name: Name of the document.
        number: Running number of the document.
        date: Date of the meeting.
        doc_file: Document file as PDF.
    """

    name = models.CharField(max_length=50)
    date = models.DateField()
    desc = models.TextField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=1, choices=[('S', 'Speculation'), ('D', 'Save the date'), ('P', 'Published')], default='S')
    short_desc = models.TextField(max_length=140, null=True, blank=True)
    

    def __str__(self):
        return self.name

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("event")
        verbose_name_plural = _("Events")
        ordering = ["-date"]
