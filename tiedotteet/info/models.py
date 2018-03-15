from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_str


class MailConfiguration(models.Model):
    """ configuration for email backend """
    host = models.CharField(max_length=50, default="mail.aalto.fi")
    port = models.CharField(max_length=10, default="587")
    username = models.CharField(max_length=50, default="tiedottaja@aalto.fi")
    password = models.CharField(max_length=50, default="salasana")
    use_tls = models.BooleanField(default=True)
    fail_silently = models.BooleanField(default=True)


class Tag(models.Model):
    title = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return smart_str(self.title)


class Category(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    order = models.IntegerField(default=0, blank=True, null=True)
    login_required = models.BooleanField(default=False)

    def __str__(self):
        return smart_str(self.title)

    def visible_messages(self):
        return Message.visible_objects.filter(category=self).order_by('end_date')

    def old_messages(self):
        return Message.old_objects.filter(category=self).order_by('end_date')


class MessageManager(models.Manager):
    def get_queryset(self):
        return super(MessageManager, self).get_queryset().filter(visible=True, start_date__lte=timezone.now(), end_date__gte=timezone.now())


class OldMessageManager(models.Manager):
    def get_queryset(self):
        return super(OldMessageManager, self).get_queryset().filter(visible=True, end_date__lt=timezone.now())


class Message(models.Model):
    header = models.CharField(max_length=250)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, related_name='messages', null=True)
    tags = models.ManyToManyField(
        Tag, related_name='messages', null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(
        default=timezone.now().date() + timedelta(days=7))
    deadline_date = models.DateField(default=timezone.now(
    ).date() + timedelta(days=7), blank=True, null=True)
    show_deadline = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)

    objects = models.Manager()
    visible_objects = MessageManager()
    old_objects = OldMessageManager()

    def __str__(self):
        return smart_str(self.header)

    def is_new(self):
        return timezone.now().date() - self.start_date < timedelta(days=7)

    def is_active(self):
        return self.start_date <= timezone.now().date() and self.end_date >= timezone.now().date() and self.visible

    def is_current(self):
        return self.start_date <= timezone.now().date() and self.end_date >= timezone.now().date()
