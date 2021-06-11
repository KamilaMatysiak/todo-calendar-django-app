from django.db import models
import datetime

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    localization = models.CharField(max_length=200)
    with_who = models.CharField(max_length=200)
    date = models.DateField("Date", default=datetime.datetime.now())

    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
