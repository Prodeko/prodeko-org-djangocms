import os

from google.oauth2 import service_account

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext_lazy as _

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


@staff_member_required
def add_to_mailchimp(request, email):
    """Main routine of this file that gets called from Django admin view.

    This routine gets called if a PendingUser is accepted from the admin panel.
    As a result the accepted user gets added to Prodeko's mailing list in mailchimp.

    Args:
        request: HttpRequest object.
        email: email address string.

    Returns:
        Nothing, appends either a success or an error
        message to Django messages depending on the outcome.

        An user must be a staff member to access this function.
    """

    try:
      client = MailchimpMarketing.Client()
      client.set_config({
        "api_key": settings.MAILCHIMP_API_KEY,
        "server": "us17"
      })

      response = client.lists.add_list_member(settings.MAILCHIMP_LIST_ID, {"email_address": email, "status": "subscribed"})

      messages.add_message(
            request,
            messages.SUCCESS,
            _("Successfully added {} to mailchimp mailing list.").format(email),
      )
    except ApiClientError as error:
        print("Error adding to mailchimp: {}".format(error.text.title))
        messages.add_message(
            request,
            messages.ERROR,
            _(
                error.text
            ),
        )
