from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Emission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    total_co2 = models.FloatField()
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.total_co2} kg CO2"

class EmissionLog(models.Model):
    """
    Comprehensive log storing all emission-related details in a single table.
    Stores: date, km_travel, electricity_units, meals (calories), co2_emission
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    date = models.DateField(default=timezone.now)
    km_travel = models.FloatField(default=0)
    electricity_units = models.FloatField(default=0)
    meals_calories = models.IntegerField(default=0)
    co2_emission = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Emission Logs"
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.co2_emission} kg CO2"
