from rest_framework import generics, permissions

from alumnirekisteri.rekisteri.models import *
from alumnirekisteri.rekisteri.serializers import *
from django.conf import settings
from auth_prodeko.models import User
from google.oauth2 import service_account
from apiclient.discovery import build

import json
import stripe
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import JsonResponse
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
import os



stripe.api_key = settings.STRIPE_API_KEY
endpoint_secret = settings.STRIPE_ENDPOINT_SECRET


def initialize_service():
    """Initializes a Google Drive API instance.

    Returns:
        Google Directory API service object.
    """

    SERVICE_ACCOUNT_FILE = os.path.join(
        settings.BASE_DIR, "prodekoorg/service_account.json"
    )

    SCOPES = ['https://www.googleapis.com/auth/drive']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, subject="mediakeisari@prodeko.org", scopes=SCOPES
    )

    return build("sheets", "v4", credentials=credentials)

def modify_sheet(sheet_id, user):
    email = user.email
    person = user.person
    service = initialize_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range="Sheet1!A1:D5").execute()
    values = result.get("values", [])
    print(values)
    if values == None:
        print("No data found.")
    else:
        current_time = datetime.datetime.now().strftime("%H:%M")
        for row in values:
            if email in row:
                # Get the current time in HH:MM format
                # Append the current time to the row
                row.append(current_time)
                body = {'values': [row]}
                row_num = values.index(row)+1
                result = sheet.values().update(spreadsheetId=sheet_id, range=f"Sheet1!{row_num}:{row_num}", valueInputOption="USER_ENTERED", body=body).execute()
                print(f"{result.get('updatedCells')} cells updated.")
                return
        # If email is not found in the sheet, append a new row with the email and current time
        row = [email, user.first_name, user.last_name, person.get_member_type_display(), current_time]
        body = {'values': [row]}
        result = sheet.values().append(spreadsheetId=sheet_id, range="Sheet1", valueInputOption="USER_ENTERED", body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
    


class Scanner(View):
    def post(self, request, *args, **kwargs):
        session_key = json.loads(request.body).get('sessionKey')
        if session_key:
            try:
                session = Session.objects.get(session_key=session_key)
                if session.expire_date > timezone.now():
                    print('Session is active')

                    # Decode the session data to retrieve the user id
                    session_data = session.get_decoded()
                    user_id = session_data.get('_auth_user_id')

                    # Fetch the user associated with this id
                    if user_id:
                        user = User.objects.get(id=user_id)
                        # Now you can use `user` object to access user data
                        # For example, user.username, user.email, etc.

                        # Add user email to sheet
                        sheet_id = '1yujAklmgLFwynul5ds_SGdzNbGwDo24XI-h2XJw7jbs'
                        try:
                            modify_sheet(sheet_id, user)
                            return JsonResponse({'active': True, 'message': 'Email added to sheet.'})
                        except HttpError as error:
                            print(f"An error occurred: {error}")
                            return JsonResponse({'active': False, 'message': 'An error occurred.'})

            except Session.DoesNotExist:
                pass
        return JsonResponse({'active': False})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhook(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.headers.get('STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return JsonResponse({'error': 'Invalid payload.'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return JsonResponse({'error': 'Invalid signature.'}, status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            cache.clear()
            checkout = event['data']['object']
            user_id = checkout['client_reference_id']
            plink_id = checkout['payment_link']

            if (plink_id == settings.STRIPE_PAYMENT_LINK_ID):
                today = datetime.date.today()
                next_due_date = datetime.date(today.year + 1, 10, 31)
                person = Person.objects.get(pk=user_id)
                person.member_until = next_due_date
                person.save()
            else:
                print('Payment link id did not match!')
        else:
            print('Unhandled event type {}'.format(event['type']))

        return JsonResponse({'success': True})


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PersonList(generics.ListAPIView):
    """ Read only. Serialize a list of persons. """

    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """ Filter queryset against GET-parameters """
        queryset = Person.objects.all()
        first_name = self.request.query_params.get("firstname", None)
        if first_name is not None:
            queryset = queryset.filter(user__first_name=first_name)
        last_name = self.request.query_params.get("lastname", None)
        if last_name is not None:
            queryset = queryset.filter(user__last_name=last_name)
        class_of_year = self.request.query_params.get("year", None)
        if class_of_year is not None and class_of_year.isdigit():
            queryset = queryset.filter(class_of_year=class_of_year)
        return queryset


class PersonDetail(generics.RetrieveAPIView):
    """ Read only. Serialize one person. """

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticated,)
