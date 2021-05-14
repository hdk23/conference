from django.shortcuts import render, reverse
from .functions_create_objects import create_committee, reset_committee, soft_reset
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .functions_read_files import read_file
from .views_my_committee import *
from .views_admin import *
from .views_context import *
from .views_pospapers import *
from .views_writing import *


# API-Related
# Google Calendar API
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from django.core.serializers.json import DjangoJSONEncoder
import json
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Conference-Related
CONFERENCE_ACRONYM = "DartMUN 2021"
conference = Conference.objects.get(acronym=CONFERENCE_ACRONYM)


# Create your views here.
def index(request):
    """loads the index page"""
    context = {}
    files = ["sessions", "categories", "modes", "motions", "organs",
            "pp_rubric", "reso_rubric", "part_rubric", "committees", "schools",
             "secretariat", "dais", "delegates"]
    simple_files = ["committees", "dais", "delegates"]
    try:
        Conference.objects.get(acronym=CONFERENCE_ACRONYM)
    except:
        Conference(acronym=CONFERENCE_ACRONYM, name="Dartmouth Model United Nations 2021").save()
    # soft_reset()
    # reset_committee()
    # for file in files:
    #     read_file(file)
    context['conference'] = conference
    return render(request, 'dartmun/index.html', context)


def call_gc_api():
    """helper method to call the Google Calendar API, returns a constructed resource using build"""
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


def secretariat(request):
    """loads the committees page to access pages specific to each committee"""
    context = {'secretariat': Secretariat.objects.all()}
    return render(request, 'dartmun/secretariat.html', context)


def committees(request, mode='my_committee'):
    """loads the committees page to access pages specific to each committee"""
    try:
        conference = get_conference(request)
    except:
        conference = Conference.objects.get(acronym=CONFERENCE_ACRONYM)
    context = {'mode': mode, 'organs': conference.organs.all()}
    return render(request, 'dartmun/committees.html', context)


def about_committee(request, committee_acronym):
    """loads the page about the committee"""
    context = {'committee': Committee.objects.get(acronym=committee_acronym)}
    return render(request, 'dartmun/committee.html', context)


@login_required(login_url='/registration/login/')
def my_committee(request, committee_acronym=None):
    """loads the my committee page"""
    if request.user.is_superuser:
        if committee_acronym:
            context = get_context(request, committee_acronym)
        else:
            return HttpResponseRedirect(reverse('committees', kwargs={'mode': 'my_committee'}))
    else:
        context = get_context(request)
    return render(request, 'dartmun/mycommittee.html', context)


@staff_member_required(login_url='/admin/login/')
def grades(request, committee_acronym=None):
    """
    loads the page that displays all delegations' grades
    recalculates delegates' scores each time
    """
    if request.user.is_superuser:
        if committee_acronym:
            context = get_context(request, committee_acronym)
        else:
            return HttpResponseRedirect(reverse('committees', kwargs={'mode': 'grades'}))
    else:
        context = get_context(request)
    context['tally_categories'] = TallyCategory.objects.all()
    if context['committee'].grades.need_update:
        context['committee'].grades.calc_grades()
    context['score_managers'] = context['committee'].grades.score_managers.order_by('delegation__country').order_by('-score')
    return render(request, 'dartmun/grades.html', context)


@staff_member_required(login_url='/admin/login/')
def tallies(request, committee_acronym=None):
    """loads a transcript of the tallies"""
    if request.user.is_superuser:
        if committee_acronym:
            context = get_context(request, committee_acronym)
        else:
            return HttpResponseRedirect(reverse('committees', kwargs={'mode': 'tallies'}))
    else:
        context = get_context(request)
    return render(request, 'dartmun/tallies.html', context)


@login_required(login_url='/registration/login/')
def resos(request, committee_acronym=None):
    """loads the writings page"""
    if request.user.is_superuser:
        if committee_acronym:
            context = get_context(request, committee_acronym)
        else:
            return HttpResponseRedirect(reverse('committees', kwargs={'mode': 'resos'}))
    else:
        context = get_context(request)
    context['reso_rubric'] = Rubric.objects.get(title="Resolution Rubric")
    context['part_rubric'] = Rubric.objects.get(title="Participation Rubric")
    context['part_tallies'] = get_category_tallies("P", "UNEP")
    return render(request, 'dartmun/resos.html', context)


@staff_member_required(login_url='/admin/login/')
def attendance(request, committee_acronym=None):
    """loads the attendance page"""
    if request.user.is_superuser:
        if committee_acronym:
            context = get_context(request, committee_acronym)
        else:
            return HttpResponseRedirect(reverse('committees', kwargs={'mode': 'attendance'}))
    else:
        context = get_context(request)
    context['sessions'] = get_conference(request).sessions.all()
    return render(request, 'dartmun/attendance.html', context)


@staff_member_required(login_url='/admin/login/')
def admin(request, committee_acronym=None):
    """admin page to add/remove delegations"""
    if request.user.is_superuser:
        if committee_acronym:
            context = get_context(request, committee_acronym)
        else:
            return HttpResponseRedirect(reverse('committees', kwargs={'mode': 'admin'}))
    else:
        context = get_context(request)
    context['countries'] = CountryField()
    taken_countries = []
    committee = get_committee(request, committee_acronym)
    for delegation in committee.people.delegations.all():
        taken_countries.append(delegation.country)
    context['taken_countries'] = taken_countries
    return render(request, 'dartmun/admin.html', context)
