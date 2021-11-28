import locale

import datefinder
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import calendar
from datetime import datetime, date, timedelta

from .models import *
from .forms import *
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.http import Http404
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

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
timezone = 'Europe/Warsaw'

def get_context(year, month, day, user):
    meetings = [x for x in Meeting.objects.all() if x.user == user]
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

    days = []
    for d in cal.itermonthdays2(year, month):
        classes = ""
        for m in meetings:
            if m.date_start.day == d[0] and m.date_start.month == month and m.date_start.year == year:
                classes += "busy "
                break
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

    timetable = []
    for i in range(24):
        timetable.append((f"{i}"":00", []))
        for j in range(15, 60, 15):
            if j % 30 == 0:
                timetable.append((f"{i}:{j}", []))
            else:
                timetable.append(("", []))

    for m in meetings:
        if m.date_start.day == day and m.date_start.month == month and m.date_start.year == year:
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


    current_week = []
    for i in range(weekday, 0, -1):
        week_day = date - timedelta(days=i)
        events = Meeting.objects.filter(user=user, date_start=week_day)
        current_week.append((week_day, events))

    for i in range(7 - weekday):
        week_day = date + timedelta(days=i)
        events = Meeting.objects.filter(user=user, date_start=week_day)
        current_week.append((week_day, events))

    context = {
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


def weekView(request, year, month, day):
    user = request.user
    context = get_context(year, month, day, user)
    return render(request, 'calendar/week.html', context)


def get_span(meeting):
    diff = ((meeting.time_end.hour - meeting.time_start.hour) * 60
            + (meeting.time_end.minute - meeting.time_start.minute)) // 15
    return diff + 1


def create_event(service, start_date_str, end_date_str, start_time_str, end_time_str, summary, description=None,
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


def current_date(request):
    now = datetime.now()
    return redirect('home', now.year, now.month, now.day)


class AddEventView(BSModalCreateView):
    template_name = 'calendar/add_meeting.html'
    form_class = EventModelForm
    success_message = "Dodano spotkanie"
    success_url = reverse_lazy('date')

    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.user = self.request.user

        # TODO: SocialToken matching query does not exist
        from google.oauth2.credentials import Credentials
        from allauth.socialaccount.models import SocialToken

        print(obj.user, "   ")
        try:
            social_token = SocialToken.objects.get(account__user=self.request.user)
            print(social_token,"   ")
            print(social_token.__dict__, "   ")
            # TODO: creds could be invalid
            creds = Credentials(token=social_token.token,
                                refresh_token=social_token.token_secret,
                                client_id=social_token.app.client_id,
                                client_secret=social_token.app.secret,
                                )
            print(creds, "= ,")
            print(creds.__dict__, "=  ")
            service = build('calendar', 'v3', credentials=creds)
            # print(service.calendars().get(calendarId='primary').execute(), "=  ")
            # calendar = service.calendars().get(calendarId='primary')
            # print(calendar)
            # print(calendar.__dict__, "=  ")
            print("start: ", obj.date_start, "\n end: ", obj.date_end)
            create_event(service=service,
                         start_date_str=obj.date_start,
                         summary=obj.title,
                         description=obj.title,
                         end_date_str=obj.date_end,
                         start_time_str=obj.time_start,
                         end_time_str=obj.time_end)
        except Exception as e:
            print("Error is", e)
        return super(AddEventView, self).form_valid(form)





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
