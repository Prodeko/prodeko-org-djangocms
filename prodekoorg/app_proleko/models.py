import datetime
from django.db import models
from django.templatetags.static import static
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


def form_upload_path(self, filename):
    return f"proleko/archives/{self.year}/{filename}"


class Lehti(models.Model):
    year = models.IntegerField(
        default=datetime.date.today().year,
        null=False,
        blank=False,
        verbose_name=_("Year"),
    )
    issue = models.IntegerField(
        default=1, null=False, blank=False, verbose_name=_("Issue")
    )
    file = models.FileField(
        unique=True, upload_to=form_upload_path, verbose_name=_("File")
    )
    thumbnail = models.ImageField(
        upload_to=form_upload_path, blank=True, verbose_name=_("Thumbnail")
    )
    title = models.CharField(max_length=255, blank=True, verbose_name=_("Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    def __str__(self):
        return self.title

    def get_thumbnail_image(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return static("/misc/default_thumbnail.jpg")

    class Meta:
        verbose_name = _("proleko")
        verbose_name_plural = _("Proleko's")
        unique_together = (
            "year",
            "issue",
        )


class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name=_("Title"), null=False)
    authors = models.CharField(max_length=255, verbose_name=_("Author"), null=True)
    ingress = models.TextField(verbose_name=_("Lead"), blank=True)
    content = RichTextUploadingField(verbose_name=_("Content"), blank=False)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, verbose_name=_("Liked by")
    )

    def total_likes(self):
        return self.likes.all().count()

    def form_upload_path(self, filename):
        return f"proleko/posts/{self.timestamp.year}/{filename}"

    thumbnail = models.ImageField(upload_to=form_upload_path, blank=True)

    def __str__(self):
        return f"{self.title} – {self.timestamp.month}/{self.timestamp.year}"

    def get_thumbnail_image(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return static("/misc/default_post_thumbnail.jpg")

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("Posts")
