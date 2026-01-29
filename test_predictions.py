#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from emissions.future_predictions import predict_future_emissions, get_user_average_metrics

# Get first user
user = User.objects.first()
if user:
    print(f'Testing with user: {user.username}')
    metrics = get_user_average_metrics(user)
    print(f'User metrics: {metrics}')
    
    predictions = predict_future_emissions(
        days_ahead=30,
        avg_travel=metrics['avg_travel'],
        avg_electricity=metrics['avg_electricity'],
        avg_fuel=metrics['avg_fuel']
    )
    
    if predictions:
        print(f'✓ Predictions generated: {len(predictions["dates"])} days')
        print(f'Sample dates: {predictions["dates"][:3]}')
        print(f'Sample values: {predictions["predictions"][:3]}')
    else:
        print('ERROR: No predictions generated')
else:
    print('No users found in database')
