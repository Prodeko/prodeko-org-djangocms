import os

from apiclient.discovery import build
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext_lazy as _
from google.oauth2 import service_account
from googleapiclient.http import HttpError


def initialize_service():
    """Initializes a Google Drive API instance.

    Returns:
        Google Directory API service object.
    """

    SERVICE_ACCOUNT_FILE = os.path.join(
        settings.BASE_DIR, "prodekoorg/service_account.json"
    )

    SCOPES = [
        "https://www.googleapis.com/auth/admin.directory.group",
        "https://www.googleapis.com/auth/admin.directory.user",
    ]

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, subject="mediakeisari@prodeko.org", scopes=SCOPES
    )
    service = build("admin", "directory_v1", credentials=credentials)
    return service


@staff_member_required
def main_groups_api(request, email, mailing_list):
    """Main routine of this file that gets called from Django admin view.

    This routine gets called if a PendingUser is accepted from the admin panel.
    As a result the accepted user gets added to Prodeko's main mailing list
    (jäsenet@prodeko.org) that resides in G Suite.

    Args:
        request: HttpRequest object.
        email: email address string.

    Returns:
        Nothing, appends either a success or an error
        message to Django messages depending on the outcome.

        A user must be a staff member to access this function.
    """

    try:
        service = initialize_service()

        data = {"email": email, "role": "MEMBER"}

        # Call G Suite API and add a member to the email list
        service.members().insert(groupKey=mailing_list, body=data).execute()

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Successfully added {} to {} mailing list.").format(email, mailing_list),
        )

    except HttpError as e:
        if e.resp.status == 409:
            messages.add_message(
                request,
                messages.ERROR,
                _(
                    "Error adding a member to {}: {} is already a member.".format(
                        mailing_list, email
                    )
                ),
            )
        elif e.resp.status == 403:
            messages.add_message(
                request,
                messages.ERROR,
                _(
                    "Invalid credentials. Check documentation and validate setup in G Suite and GCP API console."
                ),
            )
            raise
