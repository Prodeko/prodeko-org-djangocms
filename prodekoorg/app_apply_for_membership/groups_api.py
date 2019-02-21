import os

from apiclient.discovery import build
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from google.oauth2 import service_account
from googleapiclient.http import HttpError

MAILING_LIST = 'jäsenet@prodeko.org' if not settings.DEBUG else 'test@prodeko.org'


def initialize_service():
    """Initializes a Google Drive API instance.

    Returns:
        Google Directory API service object.
    """

    SERVICE_ACCOUNT_FILE = os.path.join(
        settings.BASE_DIR, 'prodekoorg/service_account.json')

    SCOPES = ['https://www.googleapis.com/auth/admin.directory.group',
              'https://www.googleapis.com/auth/admin.directory.user']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, subject='mediakeisari@prodeko.org', scopes=SCOPES)
    service = build('admin', 'directory_v1', credentials=credentials)
    return service


@staff_member_required
def main_groups_api(request, email):
    """Main routine of this file that gets called from Django admin view.

    This routine gets called if a PendingUser is accepted from the admin panel.
    As a result the accepted user gets added to Prodeko's main mailing list
    (jäsenet@prodeko.org) that resides in G Suite.

    Args:
        request: HttpRequest object.
        email: email address string.

    Returns:
        Nothing, appends either a success or an error
        messages to Django messages depending on the outcome.

        A user must be a staff member to access this function.
    """

    try:
        service = initialize_service()

        data = {'email': email, 'role': 'MEMBER'}

        # Call G Suite API and add a member to the email list
        service.members().insert(
            groupKey=MAILING_LIST, body=data).execute()

        messages.add_message(request, messages.SUCCESS, _(
            'Successfully added {} to {} mailing list.'.format(email, MAILING_LIST)))

    except HttpError as e:
        if e.resp.status == 409:
            messages.add_message(request, messages.ERROR, _(
                'Error adding a member to {}: {} is already a member.'.format(MAILING_LIST, email)))
        elif e.resp.status == 403:
            messages.add_message(request, messages.ERROR, _(
                'Invalid credentials. Check documentation and validate setup in G Suite and GCP API console.'.format(e)))
            raise


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
            groupKey=MAILING_LIST, memberKey=instance.email).execute()

    except HttpError as e:
        pass
