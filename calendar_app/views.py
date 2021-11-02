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
    #meetings = Meeting.objects.all()
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


def create_event(service, start_date_str, end_date_str, start_time_str, end_time_str, summary, description=None, location=None, attendees=None):
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
    """Shows current date in dd / mm / yyyy format

    Args:
        request: request to redirect
    Returns:
        redirection to 'home' with current year, month and day

    """
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
            create_event(service=service, start_date_str=obj.date_start, summary=obj.description, end_date_str=obj.date_end,
                         start_time_str=obj.time_start, end_time_str=obj.time_end)
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
