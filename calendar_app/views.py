import locale

import datefinder
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import calendar
from datetime import datetime, date, timedelta
import requests as api_reqs

from .models import *
from .forms import *
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.http import Http404, JsonResponse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken

months = {
    1: "Styczeń",
    2: "Luty",
    3: "Marzec",
    4: "Kwiecień",
    5: "Maj",
    6: "Czerwiec",
    7: "Lipiec",
    8: "Sierpień",
    9: "Wrzesień",
    10: "Październik",
    11: "Listopad",
    12: "Grudzień"
}

colors_calendar = {'1': {'background': '#ac725e', 'foreground': '#1d1d1d'},
                   '2': {'background': '#d06b64', 'foreground': '#1d1d1d'},
                   '3': {'background': '#f83a22', 'foreground': '#1d1d1d'},
                   '4': {'background': '#fa573c', 'foreground': '#1d1d1d'},
                   '5': {'background': '#ff7537', 'foreground': '#1d1d1d'},
                   '6': {'background': '#ffad46', 'foreground': '#1d1d1d'},
                   '7': {'background': '#42d692', 'foreground': '#1d1d1d'},
                   '8': {'background': '#16a765', 'foreground': '#1d1d1d'},
                   '9': {'background': '#7bd148', 'foreground': '#1d1d1d'},
                   '10': {'background': '#b3dc6c', 'foreground': '#1d1d1d'},
                   '11': {'background': '#fbe983', 'foreground': '#1d1d1d'},
                   '12': {'background': '#fad165', 'foreground': '#1d1d1d'},
                   '13': {'background': '#92e1c0', 'foreground': '#1d1d1d'},
                   '14': {'background': '#9fe1e7', 'foreground': '#1d1d1d'},
                   '15': {'background': '#9fc6e7', 'foreground': '#1d1d1d'},
                   '16': {'background': '#4986e7', 'foreground': '#1d1d1d'},
                   '17': {'background': '#9a9cff', 'foreground': '#1d1d1d'},
                   '18': {'background': '#b99aff', 'foreground': '#1d1d1d'},
                   '19': {'background': '#c2c2c2', 'foreground': '#1d1d1d'},
                   '20': {'background': '#cabdbf', 'foreground': '#1d1d1d'},
                   '21': {'background': '#cca6ac', 'foreground': '#1d1d1d'},
                   '22': {'background': '#f691b2', 'foreground': '#1d1d1d'},
                   '23': {'background': '#cd74e6', 'foreground': '#1d1d1d'},
                   '24': {'background': '#a47ae2', 'foreground': '#1d1d1d'}
                   }
colors_event = {'1': {'background': '#a4bdfc', 'foreground': '#1d1d1d', 'name': 'perano'},
                '2': {'background': '#7ae7bf', 'foreground': '#1d1d1d', 'name': 'riptide'},
                '3': {'background': '#dbadff', 'foreground': '#1d1d1d', 'name': 'mauve'},
                '4': {'background': '#ff887c', 'foreground': '#1d1d1d', 'name': 'salmon'},
                '5': {'background': '#fbd75b', 'foreground': '#1d1d1d', 'name': 'dandelion'},
                '6': {'background': '#ffb878', 'foreground': '#1d1d1d', 'name': 'cheese'},
                '7': {'background': '#46d6db', 'foreground': '#1d1d1d', 'name': 'cyan'},
                '8': {'background': '#e1e1e1', 'foreground': '#1d1d1d', 'name': 'grey'},
                '9': {'background': '#5484ed', 'foreground': '#1d1d1d', 'name': 'blue'},
                '10': {'background': '#51b749', 'foreground': '#1d1d1d', 'name': 'green'},
                '11': {'background': '#dc2127', 'foreground': '#1d1d1d', 'name': 'red'},
                }
timezone = 'Europe/Warsaw'


@login_required
def home(request, year, month, day):
    """Shows a map with starting point of user, based on users localization.
        If user provide name of location,
         then map will show both starting point and destination with a line connecting  them

    Args:
        request: request to return .html file
    Returns:
        .html file with a map of user starting point and places with task assigned to them

    """
    name = "usernaame"
    locale.setlocale(locale.LC_ALL, "pl_PL")
    cal = calendar.Calendar(firstweekday=0)
    date = datetime(year, month, day).date()
    month_name = months[month]
    if month == 1:
        prev = [year - 1, 12]
        next = [year, month + 1]
    elif month == 12:
        prev = [year, month - 1]
        next = [year + 1, 1]
    else:
        prev = [year, month - 1]
        next = [year, month + 1]
    previous_month_range = calendar.monthrange(prev[0], prev[1])[1]
    if day > previous_month_range:
        prev.append(previous_month_range)
    else:
        prev.append(day)
    next_month_range = calendar.monthrange(next[0], next[1])[1]
    if day > next_month_range:
        next.append(next_month_range)
    else:
        next.append(day)
    days = cal.itermonthdays2(year, month)
    daysy = cal.itermonthdays2(year, month)
    now = datetime.now()
    day_name = date.strftime("%A")
    current_day = now.day
    current_month = now.month
    # current_year = now.year
    time = datetime.now().time()
    meetings = [x for x in Meeting.objects.all() if x.user == request.user]
    # meetings = Meeting.objects.all()
    form = EventModelForm()
    return render(request,
                  'calendar/home.html',
                  {
                      "name": name,
                      "year": year,
                      "month": month,
                      "day": day,
                      "date": date,
                      "prev_month": prev,
                      "next_month": next,
                      "month_name": month_name,
                      "days": days,
                      "daysy": daysy,
                      "day_name": day_name,
                      "current_day": current_day,
                      "current_month": current_month,
                      #   "current_year": current_year,
                      "time": time,
                      "meetings": meetings,
                      "form": form
                  })


def create_event(service, start_date_str, end_date_str, start_time_str, end_time_str, description, summary=None,
                 location=None, attendees=None):
    if attendees is None:
        attendees = []

    full_start_datetime = datetime.combine(start_date_str, start_time_str)
    full_end_datetime = datetime.combine(end_date_str, end_time_str)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': full_start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': full_end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'attendees': attendees,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10}, ], }, }
    event = service.events().insert(calendarId="primary", body=event).execute()
    print(event)


def current_date(request):
    """Shows current date in dd / mm / yyyy format

    Args:
        request: request to redirect
    Returns:
        redirection to 'home' with current year, month and day

    """
    now = datetime.now()
    return redirect('home', now.year, now.month, now.day)


def build_credentials(token):
    return Credentials(token=token.token,
                       refresh_token=token.token_secret,
                       client_id=token.app.client_id,
                       client_secret=token.app.secret,
                       )


def construct_service(user):
    social_token = SocialToken.objects.get(account__user=user)
    creds = build_credentials(social_token)
    return build('calendar', 'v3', credentials=creds)


class AddEventView(BSModalCreateView):
    template_name = 'calendar/add_meeting.html'
    form_class = EventModelForm
    success_message = "Dodano spotkanie"
    success_url = reverse_lazy('date')

    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.user = self.request.user

        print(obj.user, "   ")
        try:
            service = construct_service(obj.user)
            print("start: ", obj.date_start, "\n end: ", obj.date_end)
            create_event(service=service,
                         start_date_str=obj.date_start,
                         summary=obj.title,
                         description=obj.description,
                         end_date_str=obj.date_end,
                         start_time_str=obj.time_start,
                         end_time_str=obj.time_end)
        except Exception as e:
            print("Error is", e)
        return super(AddEventView, self).form_valid(form)


@login_required
def retrieve_google_contacts(request):
    import xml.etree.ElementTree as ET

    user = request.user
    response = {}
    try:
        social_token = SocialToken.objects.get(account__user=user)

        url = 'https://www.google.com/m8/feeds/contacts/default/full' + '?access_token=' + social_token.token + '&max-results=100'
        data = api_reqs.get(url, headers={
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
        contacts_xml = ET.fromstring(data.text)
        result = []

        for entry in contacts_xml.findall('{http://www.w3.org/2005/Atom}entry'):
            for address in entry.findall('{http://schemas.google.com/g/2005}email'):
                email = address.attrib.get('address')
                result.append(email)
        response = {'msg': 'success',
                    'data': result}

    except Exception as e:
        print("Got next error when tried to get google contacts: ", e)
        response = {'msg': 'error',
                    'data': e}
    return JsonResponse(response)


@login_required
def import_google_calendar_data(request):
    import re

    user = request.user
    try:
        service = construct_service(user)

        # colors = service.colors().get().execute()
        # print('colors')

        events_result = service.events().list(calendarId='primary', timeMin=datetime.utcnow().isoformat() + 'Z',
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        for event in events:
            date_start, time_start, _ = re.split(r"[TZ]", event['start'].get('dateTime', datetime.now()))
            date_end, time_end, _ = re.split(r"[TZ]", event['end'].get('dateTime', datetime.now()))

            meeting_kwargs = {
                'user': user,
                'title': event.get('summary', 'brak tytułu'),
                'description': event.get('description', 'brak opisu'),
                'date_start': date_start,
                'time_start': time_start,
                'date_end': date_end,
                'time_end': time_end,
                'color': colors_event[event['colorId']].get('name', 'blue'),
            }

            Meeting.objects.get_or_create(**meeting_kwargs)

        response = {'msg': 'success',
                    'data': events}
    except Exception as e:
        e = 'Got this exception: ' + str(e)
        print(e)
        response = {'msg': 'error',
                    'data': e}

    return JsonResponse(response)


class DeleteEventView(BSModalDeleteView):
    template_name = 'calendar/delete_meeting.html'
    model = Meeting
    success_message = "Pomyślnie usunięto spotkanie"
    success_url = reverse_lazy('date')

    def get_object(self, queryset=None):
        obj = super(DeleteEventView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


def edit_meeting(request, pk):
    meeting = Meeting.objects.get(id=pk)
    form = EventModelForm(instance=meeting)
    if not meeting.user == request.user:
        raise Http404

    if request.method == 'POST':
        form = EventModelForm(request.POST, instance=meeting, request=request)
        if form.is_valid():
            form.save()
            return redirect('/calendar')

    context = {'form': form, 'id': pk}

    return render(request, 'calendar/edit_meeting.html', context)


def delete_meeting(request, pk):
    """Deletes meeting from meeting list

    Args:
        request: POST request
    Returns:
        redirection to delete meeting

    """
    item = Meeting.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect(current_date)
    context = {'item': item}
    return render(request, 'calendar/edit_meeting.html', context)
