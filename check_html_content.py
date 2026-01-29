#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from dashboard.views import dashboard

user = User.objects.first()
factory = RequestFactory()
request = factory.get('/dashboard/')
request.user = user

response = dashboard(request)
content = response.content.decode('utf-8')

# Search for anomaly-specific content
print("ANOMALY DETECTION HTML CHECK")
print("=" * 60)

search_terms = [
    ('🚨 Anomaly Detection Report', 'Anomaly section title'),
    ('🔴 Critical anomalies detected', 'Critical severity'),
    ('Detected Anomalies:', 'Anomaly list header'),
    ('anomaly-container', 'Anomaly container class'),
    ('Z-score:', 'Z-score label'),
    ('anomalyChart', 'Anomaly chart ID'),
]

for term, description in search_terms:
    if term in content:
        print(f"✓ Found: {description}")
    else:
        print(f"✗ Missing: {description}")

# Extract a sample of the anomaly section
print("\n" + "=" * 60)
print("SAMPLE HTML CONTENT")
print("=" * 60)

# Find the anomaly section
start_idx = content.find('🚨 Anomaly Detection Report')
if start_idx != -1:
    end_idx = content.find('</div>', start_idx) + 6
    sample = content[start_idx:min(start_idx + 500, len(content))]
    print(sample)
else:
    print("Could not find anomaly section in HTML")
