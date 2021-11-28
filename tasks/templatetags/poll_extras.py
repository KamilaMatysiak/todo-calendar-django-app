from django import template
from datetime import datetime

register = template.Library()


@register.filter
def split_timeuntil(duration):
    print(duration)
    duration = duration.replace('hours', 'godz.') \
        .replace('minutes', 'min.') \
        .replace('weeks', 'tygodnie') \
        .replace('week', 'tydzień') \
        .replace('days', 'dni') \
        .replace('day', 'dzien') \
        .replace('hour', 'godzina') \
        .replace('months', 'miesiecy') \
        .replace('month', 'miesiac') \
        .replace('minute', 'minuta')
    return duration


@register.filter
def to_datetime(task):
    date = task.date
    time = task.time
    duration = datetime.combine(date, time)
    return duration


@register.filter
def is_expired(datetime):
    if datetime <= datetime.now():
        return True
    else:
        return False


@register.filter
def passed(meeting):
    if meeting.date_end == datetime.now().date():
        if meeting.time_end < datetime.now().time():
            return True
        else:
            return False


@register.filter
def get_meeting_span(meeting):
    diff = ((meeting.time_end.hour - meeting.time_start.hour) * 60
            + (meeting.time_end.minute - meeting.time_start.minute)) // 15
    return diff + 1


@register.simple_tag
def get_width(events):
    print(events)
    return 100/len(events)

@register.filter
def get_months(week):
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

    if week[0][0].month == week[6][0].month and week[0][0].year == week[6][0].year:
        m = months[week[0][0].month]
        y = week[0][0].year
        date = f"{m} {y}"
    elif week[0][0].month != week[6][0].month and week[0][0].year == week[6][0].year:
        m1 = months[week[0][0].month]
        m2 = months[week[6][0].month]
        y = week[0][0].year
        date = f"{m1} - {m2} {y}"
    else:
        m1 = months[week[0][0].month]
        m2 = months[week[6][0].month]
        y1 = week[0][0].year
        y2 = week[6][0].year
        date = f"{m1} {y1} - {m2} {y2}"
    return date

@register.filter
def get_day(date):
    return date.day

@register.filter
def get_month(date):
    return date.month

@register.filter
def get_year(date):
    return date.year

@register.filter
def get_dayname(date):
    days = {
        "Monday": "Poniedziałek",
        "Tuesday": "Wtorek",
        "Wednesday": "Środa",
        "Thursday": "Czwartek",
        "Friday": "Piątek",
        "Saturday": "Sobota",
        "Sunday": "Niedziela",

        "poniedziałek": "Poniedziałek",
        "wtorek": "Wtorek",
        "środa": "Środa",
        "czwartek": "Czwartek",
        "piątek": "Piątek",
        "sobota": "Sobota",
        "niedziela": "Niedziela"
    }
    day = days[date.strftime("%A")]
    return day