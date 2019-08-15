import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tiedosto(models.Model):
    title = models.CharField(
        max_length=255, default="", unique=True, null=False, blank=False
    )
    thumbnail_image = models.ImageField(
        upload_to="file_thumbnail_images", null=True, blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_thumbnail_image(self):
        if self.thumbnail_image:
            return "{}".format(self.thumbnail_image.url)
        else:
            return "{}{}".format(settings.STATIC_ROOT, "/misc/default_thumbnail.jpg")

    class Meta:
        # Correct spelling in Django admin
        verbose_name_plural = _("Files")


class TiedostoVersio(models.Model):
    tiedosto = models.ForeignKey(
        Tiedosto, related_name="versions", on_delete=models.CASCADE
    )
    created_date = models.DateField(auto_now_add=True, auto_now=False)
    modified_date = models.DateField(auto_now=True)
    file = models.FileField(unique=True, upload_to="files")

    def file_name(self):
        basename, extension = os.path.splitext(os.path.basename(self.file.name))
        return basename

    def file_extension(self):
        basename, extension = os.path.splitext(os.path.basename(self.file.name))
        return extension

    def __str__(self):
        title = self.tiedosto.title
        ext = self.file_extension()
        return f"{title}: {ext}"

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("file version")
        verbose_name_plural = _("File versions")
