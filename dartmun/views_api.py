# API-Related
import os
from .models import Conference
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import reverse, render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import stripe

CONFERENCE_ACRONYM = "DartMUN 2021"
conference = Conference.objects.get(acronym=CONFERENCE_ACRONYM)

# Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
stripe.api_key = settings.STRIPE_SECRET_KEY

def call_gc_api():
    """
    helper method to call the Google Calendar API, returns a constructed resource using build
    referenced official documentation
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def add_calendar_entries(request):
    """
    adds calendar entries to the user's Google Calendar account using an API
    adds an event for each conference session
    code adapted from original
    """
    service = call_gc_api()
    for session in Conference.objects.get(acronym=CONFERENCE_ACRONYM).sessions.all():
        if session.number != 0:
            event = {
                'summary': f'{CONFERENCE_ACRONYM} Session {session.number}',
                'location': 'Zoom',
                'description': 'Attend your committee session through your committee\'s Zoom Link',
                'start': {
                    'dateTime': session.start_time,
                    'timeZone': 'America/New_York'
                },
                'end': {
                    'dateTime': session.end_time,
                    'timeZone': 'America/New_York'
                },
                'recurrence': [
                ],
                'attendees': [
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            event = json.dumps(
                event,
                sort_keys=True,
                indent=1,
                cls=DjangoJSONEncoder
            )
            json_event = json.loads(event)
            created_event = service.events().insert(calendarId="primary", body=json_event,
                                                    sendNotifications=True).execute()
            print(f"Event created: {created_event.get('htmlLink')}")
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_payment(request):
    token = request.POST.get('stripeToken')
    amount = int(request.POST.get("contribution"))
    customer = stripe.Customer.create(
        email=request.user.email,
        name=request.user.get_full_name(),
        source=token
    )

    stripe.PaymentIntent.create(
        amount=amount*100,
        currency='usd',
        payment_method_types=['card'],
        metadata={'integration_check': 'accept_a_payment'}
    )

    charge = stripe.Charge.create(
        amount=amount * 100,
        currency='usd',
        description='Support Developer',
        customer=stripe.Customer.retrieve(customer.stripe_id),
    )
    print(charge.amount)
    return HttpResponseRedirect(reverse('bio'))


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")

    return HttpResponse(status=200)


def checkout(request):
    """renders the checkout page"""
    return render(request, 'dartmun/checkout.html')
