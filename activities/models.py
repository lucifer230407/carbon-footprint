from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    
    travel_km = models.FloatField(default=0)
    electricity_kwh = models.FloatField(default=0)
    meals = models.IntegerField(default=0)
    waste_kg = models.FloatField(default=0)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
