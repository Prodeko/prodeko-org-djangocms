from django.db import models
from django.conf import settings
import os

class Course(models.Model):

    name = models.CharField(max_length=255, default="", blank=False)
    coaches = models.CharField(max_length=255, default="", blank=False)
    description = models.TextField(blank=False)
    registration = models.URLField(max_length=255)
    banner = models.ImageField(upload_to = "", null=True, blank=True)
    groupsize = models.IntegerField(blank=True)
    timing = models.CharField(max_length=255)
    open = models.BooleanField()

    def __str__(self):
        return self.name

    def get_banner_image(self):
        if self.banner:
            return '{}'.format(self.banner.url)
        else:
            return "{}{}".format(settings.STATIC_URL, "img/default_thumbnail.jpg")

    class Meta:
        verbose_name_plural = "Courses"
