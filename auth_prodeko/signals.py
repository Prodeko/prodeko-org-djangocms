from datetime import datetime

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from alumnirekisteri.rekisteri.models import Person
from prodekoorg.app_membership.models import PendingUser

from .models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_alumnregistry_profile(sender, instance, created, **kwargs):
    """Creates an alumnirekisteri Person model when a PendingUser is created.
    
    Uses Django signals (https://docs.djangoproject.com/en/2.1/topics/signals/).
    """

    if not instance.is_staff or not instance.is_superuser:
        if created:
            instance.person = Person.objects.create(
                user=instance, member_type="0", slug=instance.pk
            )
            instance.save()
        elif hasattr(instance, "pendinguser"):
            pendinguser = instance.pendinguser

            year = datetime.now().year
            member_until = datetime.strptime(f"{year}-07-31", "%Y-%m-%d")

            if pendinguser.membership_type == "TR":
                member_type = 1
            elif pendinguser.membership_type == "AL":
                member_type = 3
            elif pendinguser.membership_type == "EX":
                member_type = 2

            if pendinguser.is_ayy_member == "Y":
                ayy_member = True
            else:
                ayy_member = False

            Person.objects.filter(slug=instance.pk).update(
                city=pendinguser.hometown,
                ayy_member=ayy_member,
                class_of_year=pendinguser.start_year,
                xq_year=pendinguser.start_year,
                member_until=member_until,
                member_type=member_type,
                slug=instance.pk,
                show_name_category=False,
                show_address_category=False,
                show_personal_category=False,
                show_military_category=False,
            )


@receiver(post_save, sender=PendingUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates User model when a PendingUser is created.
    
    Uses Django signals (https://docs.djangoproject.com/en/2.1/topics/signals/).
    """

    if created:
        password = User.objects.make_random_password(length=14)
        newuser = User.objects.create_user(
            email=instance.email,
            has_accepted_policies=True,
            password=password,
            is_active=False,
            first_name=instance.first_name,
            last_name=instance.last_name,
        )
        instance.user = newuser
        instance.save()
