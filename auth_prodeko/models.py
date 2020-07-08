from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from alumnirekisteri.rekisteri.models import Person


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Main user account model.  

    Used for authenticating to Prodeko's services.

    Attributes:
        username: Not used, overrides Django's built in AbstractUser model's username field.
        email: The user's email address.
        has_accepted_policies: Designates whether the user has accepted Prodeko's privacy policy.

    Information on additional attributes (such as first_name, last_name etc.) inherited from Django User model available here:
    https://docs.djangoproject.com/en/2.1/ref/contrib/auth/
    """

    username = None
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    has_accepted_policies = models.BooleanField(
        default=False,
        verbose_name=_("Accepted privacy policy"),
        help_text=_(
            "Designates whether the user has accepted Prodeko's privacy policy."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        app_label = "auth_prodeko"
        verbose_name = _("user")
        verbose_name_plural = _("Users")
