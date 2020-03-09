from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4


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

    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    t_what = models.CharField(blank=True, max_length=140)
    t_where = models.CharField(blank=True, max_length=140)
    t_when = models.CharField(blank=True, max_length=140)
    t_why = models.CharField(blank=True, max_length=140)
    t_cost = models.CharField(blank=True, max_length=140)
    t_dc = models.CharField(blank=True, max_length=140)
    t_for_who = models.CharField(blank=True, max_length=140)
    state = models.CharField(
        max_length=1,
        choices=[("S", "Speculation"), ("D", "Save the date"), ("P", "Published")],
        default="S",
    )
    short_desc = models.TextField(max_length=140, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from .gcalendar_api import update_event

        if update_event(self):
            super().save(*args, **kwargs)
        else:
            raise ValueError("CalendarSync failed")

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("event")
        verbose_name_plural = _("Events")
        ordering = ["-start_date"]


class TapahtumaLuokat(models.Model):
    name = models.CharField(max_length=50)

