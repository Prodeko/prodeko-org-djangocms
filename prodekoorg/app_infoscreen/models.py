from datetime import timedelta

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_enddate():
    return timezone.now() + timedelta(days=7)


class Slide(models.Model):
    """Infoscreen slide.

    This model represents a slide for the guildroom infoscreen.

    Attributes:
        id: Unique id of the slide.
        title: Slide title.
        description: Slide content.
        start_datetime: Datetime to start showing the slide.
        end_datetime: Datetime to stop showing the slide.
        visible: Boolean to show or hide the slide.
    """

    title = models.CharField(max_length=50)
    description = RichTextField(config_name="main_ckeditor", blank=True)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=get_enddate)
    visible = models.BooleanField(default=True)

    def is_active(self):
        return (
            self.start_datetime <= timezone.now().date()
            and self.end_datetime >= timezone.now().date()
            and self.visible
        )

    def __str__(self):
        return self.title

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("slide")
        verbose_name_plural = _("Slides")
