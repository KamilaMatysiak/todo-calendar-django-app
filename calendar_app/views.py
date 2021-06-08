from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime

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

def home(request, year, month):
    name = "usernaame"
    cal = calendar.Calendar(firstweekday=0)
    month_name = months[month]
    days = cal.itermonthdays2(year, month)
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    time = now.strftime('%H:%M:%S %p')
    return render(request,
                  'calendar/home.html',
                  {
                      "name": name,
                      "year": year,
                      "month": month,
                      "month_name": month_name,
                      "days": days,
                      "current_month": current_month,
                      "current_year": current_year,
                      "time": time,
                  })

def current_date(request):
    now = datetime.now()
    return redirect('home', now.year, now.month)
