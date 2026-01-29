#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from emissions.models import EmissionLog
from django.contrib.auth.models import User
from datetime import datetime, timedelta

user = User.objects.first()
print(f"Adding test data for user: {user.username}\n")

# Create 5 normal days and 1 anomaly day
base_date = datetime(2026, 1, 25)
emissions_data = [
    (base_date, 2.2),
    (base_date + timedelta(days=1), 2.1),
    (base_date + timedelta(days=2), 2.3),
    (base_date + timedelta(days=3), 2.2),
    (base_date + timedelta(days=4), 2.4),
    (base_date + timedelta(days=5), 5.5),  # ANOMALY
]

for date, emission in emissions_data:
    log, created = EmissionLog.objects.get_or_create(
        user=user,
        date=date.date(),
        defaults={
            'km_travel': 10,
            'electricity_units': 5,
            'meals_calories': 2000,
            'co2_emission': emission
        }
    )
    status = "✓ Created" if created else "✓ Already exists"
    print(f"{status}: {date.date()} - {emission} kg")

print(f"\nTotal EmissionLog entries: {EmissionLog.objects.filter(user=user).count()}")
