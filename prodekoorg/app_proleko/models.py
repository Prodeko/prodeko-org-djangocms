from django.db import models

# Create your models here.
import os

from django.db import models
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
import datetime


class Lehti(models.Model):
    year = models.IntegerField(
        default=datetime.datetime.now().year, unique=True, null=False, blank=False)
    issue = models.IntegerField(default=1, null=False, blank=False)

    def form_upload_path(self, filename):
        return f"proleko/{self.year}/filename"

    file = models.FileField(unique=True, upload_to=form_upload_path)
    thumbnail = models.ImageField(unique=True, upload_to=form_upload_path)

    title = models.CharField(max_length=255, default="",
                             unique=True, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_thumbnail_image(self):
        if self.thumbnail_image:
            return f"{self.thumbnail.url}"
        else:
            return static("/misc/default_thumbnail.jpg")

    class Meta:
        verbose_name_plural = _("Prolekos")
