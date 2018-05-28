from django.db import models
from django.core.files.storage import FileSystemStorage

destination = FileSystemStorage(location='/files')

# Create your models here.

class Tiedosto(models.Model):
    file_name = models.CharField(unique=True, blank=False)
    actual_file = models.FileField(storage=destination)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True, auto_now=False)
    modified_date = models.DateField(auto_now=True)
    # filetype = models.
    actual_file = models.FileField(storage=destination)

    def
