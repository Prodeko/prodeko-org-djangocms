from rest_framework import generics, permissions

from alumnirekisteri.rekisteri.models import *
from alumnirekisteri.rekisteri.serializers import *
from django.conf import settings
from auth_prodeko.models import User

import json
import stripe
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.cache import cache


stripe.api_key = settings.STRIPE_API_KEY
endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhook(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.headers.get('STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return JsonResponse({'error': 'Invalid payload.'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return JsonResponse({'error': 'Invalid signature.'}, status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            cache.clear()
            print('Payment was successful!')
            checkout = event['data']['object']
            user_id = checkout['client_reference_id']
            plink_id = checkout['payment_link']

            if(plink_id == settings.STRIPE_PAYMENT_LINK_ID):
                today = datetime.date.today()
                next_due_date = datetime.date(today.year + 1, 10, 31)
                print('Next due date: {}'.format(next_due_date))
                print('User id: {}'.format(user_id))
                person = Person.objects.get(pk=user_id)
                print('Person: {}'.format(person.user.first_name))
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
