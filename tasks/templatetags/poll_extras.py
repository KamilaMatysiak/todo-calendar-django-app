from django import template

register = template.Library()


@register.filter
def split_timeuntil(duration):
    duration = duration.replace('hours', 'godzin') \
        .replace('minutes', 'minuty') \
        .replace('weeks', 'tygodnie') \
        .replace('days', 'dni') \
        .replace('day', 'dzien') \
        .replace('hour', 'godzina') \
        .replace('months', 'miesiecy') \
        .replace('month', 'miesiac') \
        .replace('minute', 'minuta')
    return duration
