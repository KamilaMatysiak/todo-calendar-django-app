from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

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
    date_start = models.DateField(default=now().date())
    time_start = models.TimeField(default=now().time())
    date_end = models.DateField(default=now().date())
    time_end = models.TimeField(default=now().time())

    def __str__(self):
        return self.title
