from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import calendar
from datetime import datetime, date
from .models import *
from .forms import *

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
    name = "usernaame"
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
    current_day = now.day
    current_month = now.month
    # current_year = now.year
    time = datetime.now().time()
    meetings = Meeting.objects.all()
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
                      "current_day": current_day,
                      "current_month": current_month,
                      #   "current_year": current_year,
                      "time": time,
                      "meetings": meetings
                  })


def current_date(request):
    now = datetime.now()
    return redirect('home', now.year, now.month, now.day)


def new_meeting(request):
    form = MeetingForm()

    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(current_date)

    context = {'form': form}
    return render(request, 'calendar/add_meeting.html', context)


def edit_meeting(request, pk):
    meeting = Meeting.objects.get(id=pk)
    form = MeetingForm(instance=meeting)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
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
    return render(request, 'calendar/delete_meeting.html', context)
