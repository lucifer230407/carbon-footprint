#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from emissions.models import EmissionLog
from django.contrib.auth.models import User
from dashboard.views import detect_user_anomalies, get_anomaly_summary

# Check emission data
users = User.objects.all()
print("=" * 60)
print("EMISSION DATA CHECK")
print("=" * 60)

for user in users:
    logs = EmissionLog.objects.filter(user=user).order_by('date')
    print(f"\nUser: {user.username}")
    print(f"Total EmissionLog entries: {logs.count()}")
    
    if logs.count() > 0:
        print(f"Date range: {logs.first().date} to {logs.last().date}")
        print(f"\nEmission values:")
        for log in logs:
            print(f"  {log.date}: {log.co2_emission} kg")
        
        # Check anomalies
        print("\n" + "-" * 60)
        print("ANOMALY DETECTION RESULTS")
        print("-" * 60)
        
        anomalies = detect_user_anomalies(user)
        print(f"Has anomalies: {anomalies['has_anomalies']}")
        print(f"Total checked: {anomalies['total_checked']}")
        print(f"Anomaly count: {anomalies.get('anomaly_count', 0)}")
        
        if anomalies['has_anomalies']:
            print(f"\nDetected anomalies:")
            for anom in anomalies['anomalies']:
                print(f"  Date: {anom['date']}")
                print(f"  Emission: {anom['emission']} kg")
                print(f"  Z-score: {anom['z_score']}")
                print(f"  Description: {anom['description']}\n")
        
        summary = get_anomaly_summary(user)
        print(f"Summary Status: {summary['status']}")
        print(f"Severity: {summary['severity']}")
        print(f"Count: {summary['count']}")
    else:
        print("No EmissionLog entries found!")
    
    print("\n")

print("=" * 60)
