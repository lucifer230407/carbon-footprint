#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from dashboard.views import dashboard
import re

user = User.objects.first()
factory = RequestFactory()
request = factory.get('/dashboard/')
request.user = user

response = dashboard(request)
content = response.content.decode('utf-8')

# Find the script tag
script_start = content.find('<script>')
script_end = content.find('</script>', script_start)

if script_start != -1 and script_end != -1:
    script_content = content[script_start + 8:script_end]
    
    # Check for anomaly chart code
    print("FULL SCRIPT CONTENT CHECK")
    print("=" * 70)
    
    if '// Anomaly Detection Chart' in script_content:
        print("✓ Found: Anomaly Detection Chart comment")
    else:
        print("✗ Missing: Anomaly Detection Chart comment")
    
    if 'anomalyChart' in script_content:
        print("✓ Found: anomalyChart references")
    else:
        print("✗ Missing: anomalyChart references")
    
    if 'chartDates' in script_content:
        print("✓ Found: chartDates variable")
    else:
        print("✗ Missing: chartDates variable")
    
    if 'chartCO2Values' in script_content:
        print("✓ Found: chartCO2Values variable")
    else:
        print("✗ Missing: chartCO2Values variable")
    
    print("\n" + "=" * 70)
    print("ANOMALY CHART SECTION:")
    print("=" * 70)
    
    # Extract just the anomaly chart section
    anomaly_start = script_content.find('// Anomaly Detection Chart')
    if anomaly_start != -1:
        anomaly_section = script_content[anomaly_start:anomaly_start + 1000]
        print(anomaly_section)
    else:
        print("Could not find anomaly chart section")
else:
    print("Could not find script tag")
