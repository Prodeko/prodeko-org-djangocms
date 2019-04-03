from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from prodekoorg.app_apply_for_membership.models import PendingUser
from alumnirekisteri.rekisteri.models import Person


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
#        user.person = Person.objects.create(
#            member_type='0',
#            slug=user.pk
#        )
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    has_accepted_policies = models.BooleanField(
        default=False,
        verbose_name=_('Accepted privacy and cookie policy'),
        help_text=_('Designates whether the user has accepted Prodeko\'s privacy policy and cookie policy.'))
    person = models.OneToOneField(Person, verbose_name=_('Alumn registry profile'), related_name="user", null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

    @receiver(post_save, sender=PendingUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            password = User.objects.make_random_password(length=14)
            usermodel = User.objects.create_user(
                email=instance.email,
                has_accepted_policies=True,
                password=password,
                is_active=False,
                first_name=instance.first_name,
                last_name=instance.last_name)
            instance.user = usermodel
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_alumnregistry_profile(sender, instance, created, **kwargs):
        if created:
            instance.person = Person.objects.create(
                member_type='0',
                slug=instance.pk
            )
            instance.save()

    objects = UserManager()

    class Meta:
        app_label = 'auth_prodeko'
        verbose_name = _('user')
        verbose_name_plural = _("Users")
