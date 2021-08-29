import locale

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import calendar
from datetime import datetime, date
from .models import *
from .forms import *
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView

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
    now = datetime.now()
    day_name = date.strftime("%A")
    current_day = now.day
    current_month = now.month
    # current_year = now.year
    time = datetime.now().time()
    meetings = (x for x in Meeting.objects.all() if x.user == request.user)
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
                      "day_name": day_name,
                      "current_day": current_day,
                      "current_month": current_month,
                      #   "current_year": current_year,
                      "time": time,
                      "meetings": meetings,
                      "form": form
                  })


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


class DeleteEventView(BSModalDeleteView):
    template_name = 'calendar/delete_meeting.html'
    model = Meeting
    success_message = "Pomyślnie usunięto spotkanie"
    success_url = reverse_lazy('date')


def edit_meeting(request, pk):
    meeting = Meeting.objects.get(id=pk)
    form = EventModelForm(instance=meeting)

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
