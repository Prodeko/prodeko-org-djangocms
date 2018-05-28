from django.db import models
from django.conf import settings

from django.core.files.storage import FileSystemStorage
import os

destination = FileSystemStorage(location='/files')

# Create your models here.

class Tiedosto(models.Model):
    file = models.FileField(unique=True, upload_to = "files")
    thumbnail_image = models.ImageField(upload_to = "file_thumbnail_images", null=True)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True, auto_now=False)
    modified_date = models.DateField(auto_now=True)

    def file_name(self):
        basename, extension = os.path.splitext(os.path.basename(self.file.name))
        return basename

    def file_extension(self):
        basename, extension = os.path.splitext(os.path.basename(self.file.name))
        return extension

    def get_thumbnail_image(self):
        return self.thumbnail_image.url
