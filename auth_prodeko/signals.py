from datetime import datetime

from alumnirekisteri.rekisteri.models import Person
from django.db.models.signals import post_save
from django.dispatch import receiver
from prodekoorg.app_apply_for_membership.models import PendingUser

from .models import User


def create_alumnregistry_profile(user, pendinguser):
    """Creates an alumnirekisteri Person after main user model is created."""
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

    user.person = Person.objects.create(
        user=user,
        city=pendinguser.hometown,
        ayy_member=ayy_member,
        class_of_year=pendinguser.start_year,
        xq_year=pendinguser.start_year,
        member_until=member_until,
        member_type=member_type,
        slug=user.pk,
    )
    user.save()


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

        create_alumnregistry_profile(user=newuser, pendinguser=instance)
