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
    print(len(events))
    return 4 - len(events)

