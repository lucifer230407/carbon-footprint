#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client

# Get the user
user = User.objects.first()
print(f"Testing dashboard for user: {user.username}\n")

# Create a test client and login
client = Client()
# For testing, we'll just check the view directly
from django.test import RequestFactory
from dashboard.views import dashboard

# Create a test request
factory = RequestFactory()
request = factory.get('/dashboard/')
request.user = user

# Call the dashboard view
response = dashboard(request)

# Extract context from response
if hasattr(response, 'context_data'):
    context = response.context_data
    print("Dashboard Context Variables:")
    print(f"  anomaly_summary: {context.get('anomaly_summary')}")
    print(f"  anomaly_details: {context.get('anomaly_details')}")
    print(f"  anomaly_dates: {context.get('anomaly_dates')}")
    print(f"  anomaly_values: {context.get('anomaly_values')}")
else:
    # For render responses, we need to check differently
    print("Response type:", type(response))
    print("Status code:", response.status_code)
    
    # Try to find anomaly in the rendered content
    content = response.content.decode('utf-8')
    if '🚨 Anomaly Detection Report' in content:
        print("✓ Anomaly section FOUND in rendered HTML")
    else:
        print("✗ Anomaly section NOT FOUND in rendered HTML")
    
    if 'has_anomalies' in content:
        print("✓ 'has_anomalies' found in HTML")
    else:
        print("✗ 'has_anomalies' NOT found in HTML")
