from django.db import models
from django.core.files.storage import FileSystemStorage
import os

destination = FileSystemStorage(location='/files')

# Create your models here.

class Tiedosto(models.Model):
    file = models.FileField(unique=True, upload_to = "files")
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True, auto_now=False)
    modified_date = models.DateField(auto_now=True)

    def file_name(self):
        basename, extension = os.path.splitext(os.path.basename(self.file.name))
        return basename
