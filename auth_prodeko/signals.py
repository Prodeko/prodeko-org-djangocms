from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from alumnirekisteri.rekisteri.models import Person


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_alumniregistry_profile(sender, instance, created, **kwargs):
    """Give every new account a matrikkeli profile.

    Runs when an account is created, which since the move to Keycloak
    means the first time someone signs in.
    """

    if not created:
        return

    Person.objects.create(user=instance, member_type=0, slug=str(instance.pk))
