from datetime import timedelta

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_enddate():
    return timezone.now() + timedelta(days=7)


class Slide(models.Model):
    """Infoscreen slide.

    This model represents a slide for the guildroom infoscreen.

    Attributes:
        title: Slide title.
        start_datetime: Datetime to start showing the slide.
        end_datetime: Datetime to stop showing the slide.
        description: Slide content.
        highlight: Boolean to highlight the slide.
        visible: Boolean to show or hide the slide.
    """

    title = models.CharField(verbose_name=_("title"), max_length=50)
    start_datetime = models.DateTimeField(
        verbose_name=_("start datetime"), default=timezone.now
    )
    end_datetime = models.DateTimeField(
        verbose_name=_("end datetime"), default=get_enddate
    )
    description = RichTextUploadingField(verbose_name=_("description"), blank=True)
    image = models.ImageField(
        verbose_name=_("banner image"), upload_to="infoscreen", null=True, blank=True
    )
    highlight = models.BooleanField(verbose_name=_("highlight"), default=False)
    visible = models.BooleanField(verbose_name=_("visible"), default=True)

    def is_active(self):
        return (
            self.start_datetime <= timezone.now()
            and self.end_datetime >= timezone.now()
            and self.visible
        )

    def __str__(self):
        return self.title

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("slide")
        verbose_name_plural = _("Slides")
