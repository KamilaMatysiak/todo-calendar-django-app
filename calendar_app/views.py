from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
import dateutil.relativedelta
from .models import *
from .forms import *

months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

def home(request, year, month, day):
    name = "usernaame"
    cal = calendar.Calendar(firstweekday=0)
    month_name = months[month]
    if month == 1:
        prev = [year-1, 12]
        next = [year, month+1]
    elif month == 12:
        prev = [year, month-1]
        next = [year+1, 1]
    else:
        prev = [year, month-1]
        next = [year, month+1]
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
    current_year = now.year
    time = now.strftime('%H:%M:%S %p')
    meetings = Meeting.objects.all()
    return render(request,
                  'calendar/home.html',
                  {
                      "name": name,
                      "year": year,
                      "month": month,
                      "day": day,
                      "prev_month": prev,
                      "next_month": next,
                      "month_name": month_name,
                      "days": days,
                      "current_day": f"{current_day:02d}",
                      "current_month": f"{current_month:02d}",
                      "current_year": current_year,
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

    context = {'form': form}

    return render(request, 'calendar/edit_meeting.html', context)