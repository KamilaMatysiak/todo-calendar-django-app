from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import datetime, date, time

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

    def __str__(self):
        return self.title
