from django.db import models
from django.contrib.auth.models import User

class Emission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    total_co2 = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_co2} kg CO2"
