from datetime import timedelta

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _


class MailConfiguration(models.Model):
    host = models.CharField(max_length=50, default="mail.aalto.fi")
    port = models.CharField(max_length=10, default="587")
    username = models.CharField(max_length=50, default="tiedottaja@aalto.fi")
    password = models.CharField(max_length=50, default="salasana")
    use_tls = models.BooleanField(default=True)
    fail_silently = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("mail configuration")
        verbose_name_plural = _("Mail configuration")
        db_table = "tiedotteet_mailconfiguration"


class Tag(models.Model):
    """A message category.

    Attributes:
        title: Category title.
        order: Number representing category importance.
        login_required: Boolean indicating public vs private categories.
    """

    title = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return smart_str(self.title)

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("tag")
        verbose_name_plural = _("Tags")
        db_table = "tiedotteet_tag"


class Category(models.Model):
    """A message category.

    For example, messages relating to studies, events or general information.

    Attributes:
        title: Category title.
        order: Number representing category importance.
        login_required: Boolean indicating public vs private categories.
    """

    title = models.CharField(max_length=150, blank=True, null=True)
    order = models.IntegerField(default=0, blank=True, null=True)
    login_required = models.BooleanField(default=False)

    def __str__(self):
        return smart_str(self.title)

    def visible_messages(self):
        return Message.visible_objects.filter(category=self).order_by("end_date")

    def old_messages(self):
        return Message.old_objects.filter(category=self).order_by("end_date")

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("category")
        verbose_name_plural = _("Categories")
        db_table = "tiedotteet_category"


class MessageManager(models.Manager):
    def get_queryset(self):
        return (
            super(MessageManager, self)
            .get_queryset()
            .filter(
                visible=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now(),
            )
        )


class OldMessageManager(models.Manager):
    def get_queryset(self):
        return (
            super(OldMessageManager, self)
            .get_queryset()
            .filter(visible=True, end_date__lt=timezone.now())
        )


def default_date():
    return timezone.now().date() + timedelta(days=7)


class Message(models.Model):
    """A message containing some important information.

    Attributes:
        header: Message title.
        pub_date: Publishing date of the message.
        category: Message category.
        tags: Tags associated with the message.
        start_date: Date to start showing the message.
        end_date: Date to end showing the message.
        deadline_date: Signup deadline for event messages.
        show_deadline: Boolean to show or hide the deadline date.
        visible: Boolean to show or hide the message.
        content: Message content.
        objects: Custom manager.
        visible_objects: Custom model manager that only returns visible objects.
        old_objects: Custom model manager that only returns old objects.
    """

    header = models.CharField(max_length=250)
    pub_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="messages", null=True
    )
    tags = models.ManyToManyField(Tag, related_name="messages", blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=default_date)
    deadline_date = models.DateField(default=default_date, blank=True, null=True)
    show_deadline = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    content = RichTextField(blank=True)

    objects = models.Manager()
    visible_objects = MessageManager()
    old_objects = OldMessageManager()

    def __str__(self):
        return smart_str(self.header)

    def is_new(self):
        return timezone.now().date() - self.start_date < timedelta(days=7)

    def is_active(self):
        return (
            self.start_date <= timezone.now().date()
            and self.end_date >= timezone.now().date()
            and self.visible
        )

    def is_current(self):
        return (
            self.start_date <= timezone.now().date()
            and self.end_date >= timezone.now().date()
        )

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("bulletin")
        verbose_name_plural = _("Bulletins")
        db_table = "tiedotteet_message"
