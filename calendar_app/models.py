from datetime import datetime
from django.db import models

# Create your models here.

class Meeting(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    date_time_start = models.DateTimeField(default=datetime.now())
    date_time_end = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title 