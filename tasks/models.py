from django.db import models


# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    localization = models.CharField(max_length=200)
    with_who = models.CharField(max_length=200)
    date = models.DateField("Date", auto_now=True)

    High_priority = "H"
    Medium_priority = "M"
    Low_priority = "L"
    Priorities = [
        (Low_priority, "Low"),
        (Medium_priority, "Medium"),
        (High_priority, "High")
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
