import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.cache import cache
from .models import PendingUser
import datetime
import json

stripe.api_key = settings.STRIPE_API_KEY
endpoint_secret = settings.STRIPE_ENDPOINT_SECRET


@method_decorator(csrf_exempt, name='dispatch')
def payment_webhook(self, request, *args, **kwargs):
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

        if (plink_id == settings.STRIPE_PAYMENT_LINKs_ID):
            today = datetime.date.today()
            next_due_date = datetime.date(today.year + 1, 10, 31)
            person = PendingUser.objects.get(pk=user_id)
            person.update_payment()
        else:
            print('Payment link id did not match!')
    else:
        print('Unhandled event type {}'.format(event['type']))

    return JsonResponse({'success': True})

def create_payment(request):
    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=800,
            currency='eur',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse({"error": str(e)})

