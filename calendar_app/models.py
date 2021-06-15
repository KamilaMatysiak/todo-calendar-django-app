from datetime import date, datetime
from django.db import models

# Create your models here.

class Meeting(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    date_start = models.DateField(default=date.today())
    time_start = models.TimeField(default=datetime.now().time())
    date_end = models.DateField(default=date.today())
    time_end = models.TimeField(default=datetime.now().time())
    def __str__(self):
        return self.title 