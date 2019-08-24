from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from googleapiclient.http import HttpError

from .constants import MAILING_LIST
from .groups_api import initialize_service


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def delete_user_from_mailing_list(sender, instance, **kwargs):
    """Remove a user from G Suite mailing list when a user model is deleted.

    This routine gets called if a User model is deleted.
    As a result the deleted user gets removed from Prodeko's
    main mailing list (jäsenet@prodeko.org) that resides in G Suite.

    Args:
        sender: Model sending the signal.
        instance: Instance of the model that sent the signal
        **kwargs: Any additional arguments

    Returns:
        Nothing, either removes or fails to remove a user
        from the mailing list.

        A user must be a staff member to access this function.
    """

    try:
        service = initialize_service()

        # Call G Suite API and remove a member from the email list
        service.members().delete(
            groupKey=MAILING_LIST, memberKey=instance.email
        ).execute()

    except HttpError as e:
        pass
