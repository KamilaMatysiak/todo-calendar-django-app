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
    if datetime <= datetime.now() :
        return True
    else:
        return False

@register.filter
def get_contacts(list):
    contacts = list.split("|")
    count = len(contacts)
    if count < 2:
        message = contacts[0]
    else:
        message = f"{contacts[0]} + {count-1}"
    return message

