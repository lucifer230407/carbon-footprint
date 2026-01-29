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

# Extract the JavaScript for the anomaly chart
print("ANOMALY CHART JAVASCRIPT CHECK")
print("=" * 60)

# Find the anomaly chart section
start_idx = content.find('// Anomaly Detection Chart')
if start_idx != -1:
    end_idx = content.find('{% endif %}', start_idx) + 15
    js_code = content[start_idx:end_idx]
    
    # Check for required variables
    checks = [
        ('anomalyDates', 'anomalyDates variable'),
        ('anomalyValues', 'anomalyValues variable'),
        ('chartDates', 'chartDates variable'),
        ('chartCO2Values', 'chartCO2Values variable'),
        ('anomalyChart', 'anomalyChart canvas'),
        ('new Chart', 'Chart.js initialization'),
        ('scatter', 'scatter chart type'),
    ]
    
    print("JavaScript Variables and Functions:")
    for term, desc in checks:
        if term in js_code:
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc} - MISSING!")
    
    print("\n" + "=" * 60)
    print("Chart Configuration:")
    print("=" * 60)
    
    if 'type: "scatter"' in js_code:
        print("  ✓ Chart type: scatter")
    if 'Anomalies Detected' in js_code:
        print("  ✓ Dataset 1: Anomalies Detected (red points)")
    if 'All Emissions (Reference)' in js_code:
        print("  ✓ Dataset 2: All Emissions Reference (green line)")
    
    print("\n" + "=" * 60)
    print("Anomaly Dataset Mapping:")
    print("  X-axis: anomalyDates")
    print("  Y-axis: anomalyValues")
    print("\nReference Dataset Mapping:")
    print("  X-axis: chartDates")
    print("  Y-axis: chartCO2Values")
    print("=" * 60)
    
else:
    print("Could not find anomaly chart JavaScript")
