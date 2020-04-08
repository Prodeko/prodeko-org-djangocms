import datetime
from django.db import models
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Lehti(models.Model):
    year = models.IntegerField(
        default=datetime.date.today().year, null=False, blank=False)
    issue = models.IntegerField(default=1, null=False, blank=False)

    def form_upload_path(self, filename):
        return f"proleko/archives/{self.year}/{filename}"

    file = models.FileField(unique=True, upload_to=form_upload_path)
    thumbnail = models.ImageField(upload_to=form_upload_path, blank=True)

    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_thumbnail_image(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return static("/misc/default_thumbnail.jpg")

    class Meta:
        verbose_name_plural = _("Prolekos")
        unique_together = ('year', 'issue',)


class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(
        max_length=255, verbose_name="Otsikko", null=False)
    authors = models.CharField(
        max_length=255, verbose_name="Kirjoittaja", null=True)
    ingress = models.TextField(
        verbose_name=_("Ingressi"), blank=True)
    content = RichTextUploadingField(
        verbose_name=_("Sisältö"), blank=False)

    def form_upload_path(self, filename):
        return f"proleko/posts/{self.timestamp.year}/{filename}"

    thumbnail = models.ImageField(
        upload_to=form_upload_path, blank=True)

    def likes(self):
        # TODO: implement like system
        return 0

    def __str__(self):
        return f"{self.title} – {self.timestamp.month}/{self.timestamp.year}"

    def get_thumbnail_image(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return static("/misc/default_post_thumbnail.jpg")

    class Meta:
        verbose_name_plural = _("Posts")
