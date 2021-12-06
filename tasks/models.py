from django.db import models
from calendar_app.models import Meeting
from datetime import datetime, date, time
from django.forms import CheckboxInput
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

def temporary_user_validation(user):
    users = User.objects.all()
    if user not in users:
        raise ValidationError(
            "Nie ma takiego użytkownika!"
        )


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=1)
    title = models.CharField(max_length=30, primary_key=False)

    def __str__(self):
        return f"{self.title}"

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=1)
    title = models.CharField(max_length=200)
    localization = models.CharField(max_length=200)
    l_lat = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True, default=None)
    l_lon = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True, default=None)
    with_who = models.CharField(max_length=200)
    date = models.DateField(default=date.today, null=True)
    time = models.TimeField(default=datetime.now)
    High_priority = "H"
    Medium_priority = "J"
    Low_priority = "L"
    None_priority = "N"
    Priorities = [
        (None_priority, "---"),
        (Low_priority, "Niski"),
        (Medium_priority, "Średni"),
        (High_priority, "Wysoki")
    ]
    priority = models.CharField(
        max_length=10,
        choices=Priorities,
        default=None_priority
    )
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, default=1)
    from_who = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='+', validators=[temporary_user_validation])
    accepted = models.BooleanField(default=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        """Returns title of task"""
        return f"{self.title}"

    class Meta:
        ordering = ['complete', 'priority', 'date', 'title', 'localization']


