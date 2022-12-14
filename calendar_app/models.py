from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import datetime, timedelta, time, date

User = get_user_model()


class Meeting(models.Model):
    """
    user with unique key,
    title and description  as plain text,
    date of start and end,
    time of start and end
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=1)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    date_start = models.DateField(default=datetime.now)
    time_start = models.TimeField(default=datetime.now)
    date_end = models.DateField(default=datetime.now)
    time_end = models.TimeField(default=datetime.now)
    color = models.CharField(default="blue", max_length=50)
    cyclical = models.CharField(max_length=20, blank=True, null=True)
    is_cyclical = models.BooleanField(default=False)
    cycle_interval = models.CharField(max_length=10, null=True, default='d')
    cycle_number = models.IntegerField(null=True, default=1)

    with_who = models.CharField(null=True, max_length=200)
    localization = models.CharField(null=True, max_length=200)
    l_lat = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True, default=None)
    l_lon = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date_start', 'time_start', 'title']


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=1)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True, max_length=250)
