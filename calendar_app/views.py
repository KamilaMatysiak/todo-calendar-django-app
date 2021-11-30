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

from .custom_variables import colors_event, colors_calendar, months, timezone, vtodo_colors_event

def get_meetings(dict, date):
    if date in dict:
        return dict[date]
    else:
        return []

def get_context(year, month, day, user):
    meetings = Meeting.objects.filter(user=user)
    now = datetime.now()
    current_day = now.day
    current_month = now.month
    date = datetime(year, month, day).date()
    weekday = date.weekday()
    month_name = months[month]
    day_name = date.strftime("%A")
    time = datetime.now().time()
    cal = calendar.Calendar(firstweekday=0)
    form = EventModelForm()

    all_events = {}
    for m in meetings:
        meeting_date = m.date_start
        if meeting_date in all_events:
            all_events[meeting_date].append(m)
        else:
            all_events[meeting_date] = [m]

    days = []
    for d in cal.itermonthdays2(year, month):
        classes = ""
        if d[0] != 0:
            if get_meetings(all_events, datetime(year, month, d[0]).date()):
                classes += "busy "
        if d[0] == day:
            classes += "current "
        if month == current_month and d[0] == current_day:
            classes += "active-day "
        if month == current_month and d[0] < current_day:
            classes += "passed-day "
        if classes == "":
            classes = "day"
        days.append([d, classes])

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

    #stuff for day
    timetable = []
    for i in range(24):
        timetable.append((f"{i}"":00", []))
        for j in range(15, 60, 15):
            if j % 30 == 0:
                timetable.append((f"{i}:{j}", []))
            else:
                timetable.append(("", []))

    for m in get_meetings(all_events, date):
        interval = m.time_start.hour * 4 + m.time_start.minute // 15
        timetable[interval][1].append(m)
    max_width = 1
    tt_width = [["", []] for i in range(24 * 60 // 15)]

    for index, (label, time_period) in enumerate(timetable):
        tt_width[index][0] = label
        for event in time_period:
            length = get_span(event)
            tt_width[index][1].append(event)
            for j in range(1, length):
                if (index + j) < len(tt_width):
                    tt_width[index + j][1].append("busy")
        if len(tt_width[index][1]) > max_width:
            max_width = len(tt_width[index][1])

    # print(timetable)
    for x in tt_width:
        string = ""
        for y in x[1]:
            string += " " + str(y)
        # print(f"{x[0]}|{string}")
    print("Maksymalna szerokosc to ", max_width)


    #stuff for week
    current_week = []
    for i in range(weekday, 0, -1):
        week_day = date - timedelta(days=i)
        current_week.append((week_day, get_meetings(all_events, week_day)))

    for i in range(7 - weekday):
        week_day = date + timedelta(days=i)
        current_week.append((week_day, get_meetings(all_events, week_day)))

    context = {
        "all_events": all_events,
        "now": now,
        "current_day": current_day,
        "current_month": current_month,
        "date": date,
        "month_name": month_name,
        "day_name": day_name,
        "time": time,
        "cal": cal,
        "days": days,
        "year": year,
        "month": month,
        "day": day,
        "prev_month": prev,
        "next_month": next,
        "meetings": meetings,
        "form": form,
        "timetable": timetable,
        "week": current_week,
    }

    return context

@login_required
def home(request, year, month, day):
    locale.setlocale(locale.LC_ALL, "pl_PL")
    user = request.user
    context = get_context(year, month, day, user)
    return render(request, 'calendar/home.html', context)


@login_required
def weekView(request, year, month, day):
    user = request.user
    context = get_context(year, month, day, user)
    return render(request, 'calendar/week.html', context)


@login_required
def monthView(request, year, month, day):
    user = request.user
    context = get_context(year, month, day, user)
    all_events = context["all_events"]
    days = context["days"]
    month_days = []
    for day, _ in days:
        if day[0] != 0:
            date = datetime(year, month, day[0]).date()
            month_days.append((day, get_meetings(all_events, date)))
        else:
            month_days.append((day, []))
    context["month_days"] = month_days
    return render(request, 'calendar/month.html', context)


def get_span(meeting):
    diff = ((meeting.time_end.hour - meeting.time_start.hour) * 60
            + (meeting.time_end.minute - meeting.time_start.minute)) // 15
    return diff + 1


def create_event(service, location=None, attendees=None, meeting_obj=None):
    if meeting_obj:
        if attendees is None:
            attendees = []

        start_date_str = meeting_obj.date_start
        summary = meeting_obj.title
        description = meeting_obj.description
        end_date_str = meeting_obj.date_end
        start_time_str = meeting_obj.time_start
        end_time_str = meeting_obj.time_end
        calendarId = meeting_obj.user.email

        full_start_datetime = datetime.combine(start_date_str, start_time_str)
        full_end_datetime = datetime.combine(end_date_str, end_time_str)

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'status': 'confirmed',
            'visibility': 'default',
            'colorId': vtodo_colors_event.get(meeting_obj.color, 'blue'),
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
                    {'method': 'popup', 'minutes': 10}, ],
            },
        }

        event = service.events().insert(calendarId=calendarId, body=event).execute()
        print(event)


def current_date(request):
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

        if self.request.is_ajax():
            try:
                service = construct_service(obj.user)
                print("start: ", obj.date_start, "\n end: ", obj.date_end)
                create_event(service=service,
                             meeting_obj=obj)
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
            print(event)
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
                'color': colors_event[event.get('colorId', '9')].get('name', 'blue'),
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
    item = Meeting.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect(current_date)
    context = {'item': item}
    return render(request, 'calendar/edit_meeting.html', context)
