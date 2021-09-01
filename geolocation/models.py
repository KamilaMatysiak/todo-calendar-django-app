from django.db import models


# Create your models here.

# class Localization(models.Model):
#     # location = models.CharField(max_length=200)
#     # destination = models.CharField(max_length=200)
#     # distance = models.DecimalField(max_digits=10, decimal_places=2)
#     # created = models.DateTimeField(auto_now_add=True)
#     l_lat = models.DecimalField(max_digits=15, decimal_places=10)
#     l_lon = models.DecimalField(max_digits=15, decimal_places=10)

#     def __str__(self):
#         # unique_together = (("l_lat","l_lon"),)
#         # constraints = [
#         #     models.UniqueConstraint(fields=['l_lat', 'l_lon'], name='LocalizationContraint')
#         # ]
#         return self
