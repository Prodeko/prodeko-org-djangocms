from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from alumnirekisteri.rekisteri.models import Person


def free_slug(base: str) -> str:
    """A slug nobody holds, derived from ``base``.

    ``Person.slug`` is unique and legacy rows carry numeric slugs of
    their own, so the primary key a new account gets can be taken
    already. Numbered suffixes are appended the way ``Person.save()``
    does, because there is no reasonable way for the person to recover
    from an IntegrityError raised at their first sign-in.
    """
    slug = base
    counter = 0
    while Person.objects.filter(slug=slug).exists():
        counter += 1
        slug = f"{base}-{counter}"
    return slug


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_alumniregistry_profile(sender, instance, created, **kwargs):
    """Give every new account a matrikkeli profile.

    Runs when an account is created, which is the first time someone
    signs in through Keycloak.
    """

    if not created:
        return

    Person.objects.create(
        user=instance, member_type=0, slug=free_slug(str(instance.pk))
    )
