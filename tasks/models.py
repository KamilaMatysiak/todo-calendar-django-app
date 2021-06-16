from django.db import models
from datetime import date


# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    localization = models.CharField(max_length=200)
    with_who = models.CharField(max_length=200)
    date = models.DateField(default=date.today())
    High_priority = "H"
    Medium_priority = "M"
    Low_priority = "L"
    Priorities = [
        (Low_priority, "Niski"),
        (Medium_priority, "Średni"),
        (High_priority, "Wysoki")
    ]
    priority = models.CharField(
        max_length=10,
        choices=Priorities,
        default=Low_priority
    )
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
