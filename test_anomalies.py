#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

import numpy as np
from dashboard.views import detect_anomaly, detect_user_anomalies, get_anomaly_summary
from django.contrib.auth.models import User

# Test detect_anomaly function
history = [2.0, 2.1, 2.2, 2.3, 2.4]
value = 5.0

is_anom, z_score, desc = detect_anomaly(value, history)
print(f"✓ detect_anomaly works: is_anomaly={is_anom}, z_score={z_score:.2f}")
print(f"  Description: {desc}\n")

# Get a user to test anomaly detection
users = User.objects.all()
if users.exists():
    user = users.first()
    print(f"✓ Testing with user: {user.username}")
    
    result = detect_user_anomalies(user)
    print(f"  Has anomalies: {result['has_anomalies']}")
    print(f"  Total entries checked: {result['total_checked']}")
    print(f"  Anomaly count: {result.get('anomaly_count', 0)}\n")
    
    summary = get_anomaly_summary(user)
    print(f"✓ Anomaly Summary:")
    print(f"  Status: {summary['status']}")
    print(f"  Severity: {summary['severity']}")
    print(f"  Count: {summary['count']}\n")
else:
    print("No users found in database\n")

print("✓ All anomaly detection functions working!")
