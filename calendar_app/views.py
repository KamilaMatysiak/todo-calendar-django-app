import locale

import datefinder
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import calendar
from datetime import datetime, date, timedelta
import requests as api_reqs
from django.http import HttpResponseRedirect
from .models import *
from tasks.models import Task
from .forms import *
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.http import Http404, JsonResponse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken
from dateutil import relativedelta
import re
from allauth.socialaccount.models import SocialToken, SocialAccount
from geopy.geocoders import Nominatim
from tasks.utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
from geopy.distance import geodesic

from .custom_variables import colors_event, colors_calendar, months, timezone, vtodo_colors_event


def is_google_user(user):
    resp = SocialAccount.objects.filter(user=user).first()
    print(resp)
    return True if resp else False


def get_meetings(dict, date):
    if date in dict:
        return dict[date]
    else:
        return []


def add_days(date, interval, number):
    if interval == 'd':
        d = timedelta(days=number)
    elif interval == 'w':
        d = timedelta(weeks=number)
    elif interval == 'm':
        d = relativedelta.relativedelta(months=number)
    elif interval == 'y':
        d = relativedelta.relativedelta(years=number)
    date += d
    return (date)


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
        if m.is_cyclical:
            next_month = date + relativedelta.relativedelta(months=1)
            next_month = next_month.replace(day=1)
            if m.date_start < next_month:
                temp_date = m.date_start
                while temp_date < next_month:
                    temp_date = add_days(temp_date, m.cycle_interval, m.cycle_number)
                    if temp_date.month == month:
                        if temp_date in all_events:
                            all_events[temp_date].append(m)
                        else:
                            all_events[temp_date] = [m]

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

    current_week = []
    for i in range(weekday, 0, -1):
        week_day = date - timedelta(days=i)
        current_week.append((week_day, get_meetings(all_events, week_day)))

    for i in range(7 - weekday):
        week_day = date + timedelta(days=i)
        current_week.append((week_day, get_meetings(all_events, week_day)))

    timetable = []
    for i in range(24):
        timetable.append((f"{i}"":00", []))
        for j in range(15, 60, 15):
            timetable.append(("", []))

    for m in get_meetings(all_events, date):
        interval = m.time_start.hour * 4 + m.time_start.minute // 15
        timetable[interval][1].append(m)

    week_timetable = []
    for i in range(24):
        week_timetable.append((f"{i}"":00", [[], [], [], [], [], [], []]))
        for j in range(15, 60, 15):
            week_timetable.append(("", [[], [], [], [], [], [], []]))

    for i, (week_day, week_meetings) in enumerate(current_week):
        for m in week_meetings:
            interval = m.time_start.hour * 4 + m.time_start.minute // 15
            week_timetable[interval][1][i].append(m)

    max_width = 1
    tt_width = [["", []] for i in range(24 * 60 // 15)]

    for index, (label, time_period) in enumerate(timetable):
        tt_width[index][0] = label
        delayed = tt_width[index][1].count("temp")
        for i, event in enumerate(time_period):
            length = get_span(event)
            if delayed > 0:
                tt_width[index][1].insert(event)
                tt_width[index][1].remove("temp")
                delayed -= 1
            tt_width[index][1].append(event)
            for j in range(1, length):
                if (index + j) < len(tt_width):
                    while len(tt_width[index + j][1]) < i - 1:
                        tt_width[index + j][1].append("temp")
                    tt_width[index + j][1].append("busy")
        if len(tt_width[index][1]) > max_width:
            max_width = len(tt_width[index][1])

    for i, (timestamp, x) in enumerate(tt_width):
        for y, cell in enumerate(x):
            if cell not in ["empty", "busy", "temp"]:
                tt_width[i][1][y] = (cell, get_span(cell), 100 // len(x), y)
        while len(x) < max_width:
            x.append("empty")

    max_week_width = [1, 1, 1, 1, 1, 1, 1]
    wtt_width = [["", [[], [], [], [], [], [], []]] for i in range(24 * 60 // 15)]
    for day_number in range(len(current_week)):
        for index, (label, time_periods) in enumerate(week_timetable):
            wtt_width[index][0] = label
            delayed = wtt_width[index][1][day_number].count("temp")
            for i, event in enumerate(time_periods[day_number]):
                length = get_span(event)
                if delayed > 0:
                    wtt_width[index][1][day_number].insert(event)
                    wtt_width[index][1][day_number].remove("temp")
                    delayed -= 1
                wtt_width[index][1][day_number].append(event)
                for j in range(1, length):
                    if (index + j) < len(wtt_width):
                        while len(wtt_width[index + j][1][day_number]) < i - 1:
                            wtt_width[index + j][1][day_number].append("temp")
                        wtt_width[index + j][1][day_number].append("busy")
            if len(wtt_width[index][1][day_number]) > max_week_width[day_number]:
                max_week_width[day_number] = len(wtt_width[index][1][day_number])

        for i, (timestamp, x) in enumerate(wtt_width):
            for y, cell in enumerate(x[day_number]):
                if cell not in ["empty", "busy", "temp"]:
                    wtt_width[i][1][day_number][y] = (cell, get_span(cell), 100 // len(x[day_number]), y)
            while len(x) < max_week_width[day_number]:
                x.append("empty")

    meetings_widths = [["", []] for i in range(24 * 60 // 15)]
    for x, m in timetable:
        if len(m) > 1:
            width = 100 / len(m)
            meetings_widths.append(width)
        elif len(m) == 1:
            width = 100
            meetings_widths.append(width)
        else:
            width = 0
            meetings_widths.append(width)

    scrollPos = int(now.hour) * 80

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
        "week_timetable": week_timetable,
        "tt_width": tt_width,
        "wtt_width": wtt_width,
        "week": current_week,
        "scrollPos": scrollPos,
        'API_KEY': settings.GOOGLE_API_KEY,
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
    height = (diff + 1)
    return height


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
        if obj.localization:
            geolocator = Nominatim(user_agent='measurements')
            destination_ = form.cleaned_data.get('localization')
            destination = geolocator.geocode(destination_)
            obj.l_lat = destination.latitude
            obj.l_lon = destination.longitude
        with_who = self.request.POST.getlist("with_who")
        obj.with_who = "|".join(with_who)
        if not form.cleaned_data['is_cyclical']:
            obj.cycle_interval = None
            obj.cycle_number = None
        if self.request.is_ajax():
            try:
                service = construct_service(obj.user)
                print("start: ", obj.date_start, "\n end: ", obj.date_end)
                create_event(service=service,
                             meeting_obj=obj)
            except Exception as e:
                print("Error is", e)
        return super(AddEventView, self).form_valid(form)


class AddNoteView(BSModalCreateView):
    template_name = 'calendar/add_note.html'
    form_class = NoteModelForm
    success_message = "Dodano notatkę"

    def get_object(self, quaryset=None):
        return super(AddNoteView, self).get_object()

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        meeting = Meeting.objects.get(pk=self.kwargs["meeting_pk"])
        obj.meeting = meeting
        self.success_url = reverse_lazy("edit_meeting", args=[obj.meeting.id])
        return super(AddNoteView, self).form_valid(form)


class EditNoteView(BSModalUpdateView):
    model = Notes
    template_name = 'calendar/edit_note.html'
    form_class = NoteModelForm
    success_message = "Zedytowano notatkę"

    def get_object(self, queryset=None):
        obj = super(EditNoteView, self).get_object()
        self.success_url = reverse_lazy("edit_meeting", args=[obj.meeting.id])
        if not obj.user == self.request.user:
            raise Http404
        return obj


class DeleteNoteView(BSModalDeleteView):
    template_name = 'calendar/delete_note.html'
    model = Notes
    success_message = "Pomyślnie usunięto notatkę"

    def get_object(self, queryset=None):
        obj = super(DeleteNoteView, self).get_object()
        self.success_url = reverse_lazy("edit_meeting", args=[obj.meeting.id])
        if not obj.user == self.request.user:
            raise Http404
        return obj


def parse_google_date(data):
    parsed = re.split(r"[TZ]", data.get('dateTime', datetime.now()))
    _date, _time = parsed[:2]
    if any(s in _time for s in ('+', '-')):
        _time = re.split(r'[+-]', _time)[0]
    return _date, _time


@login_required
def import_google_calendar_data(request):
    def construct_response(msg, data):
        return {'msg': msg,
                'data': data}

    user = request.user
    if is_google_user(user):
        try:
            service = construct_service(user)

            events_result = service.events().list(calendarId='primary', timeMin=datetime.utcnow().isoformat() + 'Z',
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])
            for event in events:
                print(event)
                date_start, time_start = parse_google_date(event['start']) \
                    if event['start'].get('dateTime') else (event['start']['date'], '00:00:00')
                date_end, time_end = parse_google_date(event['end']) \
                    if event['end'].get('dateTime') else (event['end']['date'], '23:59:00')

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

            response = construct_response('success', events)
        except Exception as e:
            e = 'Got this exception: ' + str(e)
            print(e)
            response = construct_response('error', e)
    else:
        response = construct_response('issue', 'not google')

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

        print(self.request.user)
        print(obj.__dict__)
        service = construct_service(self.request.user)
        events_items = \
            service.events().list(calendarId='primary', timeMin=datetime.utcnow().isoformat() + 'Z', singleEvents=True,
                                  orderBy='startTime').execute()['items']
        for item in events_items:
            print(item)
            date_start, time_start = parse_google_date(item['start'])
            date_end, time_end = parse_google_date(item['end'])
            if obj.title == item['summary'] and obj.description == item['description'] \
                    and str(obj.date_start) == date_start and str(obj.date_end) == date_end:
                print('PASSED')
                # kwargs = {'calendarId': 'primary',
                #           'eventId': item['id'],
                #           'sendNotifications': False}
                # service.events().delete(**kwargs).execute()
        return obj


def edit_meeting(request, pk):
    count = 0
    meeting = Meeting.objects.get(id=pk)

    form = EventModelForm(instance=meeting)
    if not meeting.user == request.user:
        raise Http404

    if request.method == 'POST':
        form = EventModelForm(request.POST, instance=meeting, request=request)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.localization:
                geolocator = Nominatim(user_agent='measurements')
                destination_ = form.cleaned_data.get('localization')
                destination = geolocator.geocode(destination_)
                obj.l_lat = destination.latitude
                obj.l_lon = destination.longitude
            with_who = request.POST.getlist("with_who")
            obj.with_who = "|".join(with_who)
            if not obj.is_cyclical:
                obj.cycle_interval = None
                obj.cycle_number = None
            obj.save()
            form.save()
            return redirect('/calendar')

    tasks = [x for x in Task.objects.all() if x.user == request.user]
    for x in tasks:
        if x.meeting == meeting:
            count += 1

    notes = [x for x in Notes.objects.all() if x.user == request.user]

    context = {
        'form': form,
        'id': pk,
        'meeting': meeting,
        'tasks': tasks,
        'count': count,
        'notes': notes,
        'API_KEY': settings.GOOGLE_API_KEY}

    return render(request, 'calendar/edit_meeting.html', context)


class ConnectTaskView(BSModalUpdateView):
    model = Meeting
    template_name = 'calendar/connect_tasks.html'
    form_class = ConnectTaskForm
    success_message = "Podpięto zadania"

    def get_form_kwargs(self):
        kwargs = super(ConnectTaskView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self):
        obj = super(ConnectTaskView, self).get_object()
        self.success_url = reverse_lazy("edit_meeting", args=[obj.id])
        self.initial['tasks'] = Task.objects.filter(meeting=obj)
        return obj

    def form_valid(self, form):
        tasks = Task.objects.filter(user=self.request.user, meeting=self.object)
        if "tasks" not in form.cleaned_data:
            form.cleaned_data["tasks"] = []
        for task in tasks:
            if task not in form.cleaned_data["tasks"]:
                task.meeting = None
                task.save()
        for task in form.cleaned_data["tasks"]:
            task.meeting = self.object
            task.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.form_valid(form)


def delete_meeting(request, pk):
    item = Meeting.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect(current_date)
    context = {'item': item}
    return render(request, 'calendar/edit_meeting.html', context)
