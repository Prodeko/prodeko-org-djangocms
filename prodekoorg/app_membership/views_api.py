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
def payment_webhook(request, *args, **kwargs):
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
    if event['type'] != 'payment_intent.succeeded':
        return JsonResponse({'error': 'Not payment_intent.succeeded.'}, status=400)
    
    cache.clear()
    payment_intent_id = event['data']['object']['id']

    if payment_intent_id is None:
        return JsonResponse({'error': 'No payment intent id.'}, status=400)

    person = PendingUser.objects.get(payment_intent_id=payment_intent_id)
    person.update_payment()

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
            }
        )
        return JsonResponse({
            'clientSecret': intent['client_secret'],
            'intentId': intent['id'],
        })
    except Exception as e:
        return JsonResponse({"error": str(e)})

