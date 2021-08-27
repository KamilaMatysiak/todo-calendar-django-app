from django.db import models


# Create your models here.

class Measurement(models.Model):
    """Location and destination as plain text,
     distance in kilometers with 2 decimal places,
      date of creation"""
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is {self.distance} km"
