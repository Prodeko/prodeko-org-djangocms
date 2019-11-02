from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _


class Course(models.Model):
    """Prodeko lifelonglearning course.

    This model represents a course in Prodeko's lifelonglearning programme.

    Attributes:
        name: Course title.
        coaches: Course coaches.
        description: Course description.
        registration: Registration form url.
        banner: Course image banner.
        groupsize: Course size in persons.
        timing: Date or dates of the course.
        open: Whether the course is open or not.
    """

    name = models.CharField(
        verbose_name=_("name"), max_length=255, default="", blank=False
    )
    coaches = models.CharField(
        verbose_name=_("coaches"), max_length=255, default="", blank=True
    )
    description = RichTextField(verbose_name=_("description"), blank=True)
    registration = models.URLField(verbose_name=_("registration url"), max_length=255)
    banner = models.ImageField(
        verbose_name=_("banner image"),
        upload_to="lifelonglearning",
        null=True,
        blank=True,
    )
    groupsize = models.IntegerField(verbose_name=_("group size"), blank=True, null=True)
    timing = models.CharField(
        verbose_name=_("timing"), max_length=255, blank=True, null=True
    )
    open = models.BooleanField(verbose_name=_("open"))

    def __str__(self):
        return self.name

    def get_banner_image(self):
        if self.banner:
            return self.banner.url
        else:
            return static("images/backgrounds/bg-blue.jpg")

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("Courses")
