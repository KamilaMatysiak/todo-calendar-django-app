from django import template

register = template.Library()


@register.filter
def split_timeuntil(duration):
    duration = duration.replace('hours', 'godziny') \
        .replace('minutes', 'minuty') \
        .replace('weeks', 'tygodnie') \
        .replace('days', 'dni')
    return duration
