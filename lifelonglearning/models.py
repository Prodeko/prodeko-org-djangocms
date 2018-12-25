from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Course(models.Model):

    name = models.CharField(max_length=255, default="", blank=False)
    coaches = models.CharField(max_length=255, default="", blank=True)
    description = RichTextField(config_name='main_ckeditor', blank=True)
    registration = models.URLField(max_length=255)
    banner = models.ImageField(upload_to="", null=True, blank=True)
    groupsize = models.IntegerField(blank=True, null=True)
    timing = models.CharField(max_length=255, blank=True, null=True)
    open = models.BooleanField()

    def __str__(self):
        return self.name

    def get_banner_image(self):
        if self.banner:
            return '{}'.format(self.banner.url)
        else:
            return "{}{}".format(settings.STATIC_URL, "img/default_thumbnail.jpg")

    class Meta:
        verbose_name = _('courses')
        verbose_name_plural = _("Courses")
