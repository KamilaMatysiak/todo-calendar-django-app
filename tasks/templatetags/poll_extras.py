from django import template

register = template.Library()


@register.filter
def split_timeuntil(duration):
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
