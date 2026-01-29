from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from emissions.models import Emission, EmissionLog
from emissions.services import generate_tips
from emissions.future_predictions import predict_future_emissions, get_user_average_metrics
from django.db.models import Sum
from django.db.models.functions import TruncDate
import json
import numpy as np

# Healthy emission target (kg CO2 per day)
HEALTHY_EMISSION_TARGET = 2.5  # Global average for sustainable living


# Anomaly Detection Functions
def detect_anomaly(value, history, threshold=2.5):
    """Detect anomalies using Z-score method."""
    if not history or len(history) < 2:
        return False, 0.0, "Not enough historical data"
    
    history = np.array(history, dtype=float)
    mean = np.mean(history)
    std = np.std(history)
    
    if std == 0:
        is_anomaly = abs(value - mean) > mean * 0.5
        return is_anomaly, 0.0, "Deviation from constant baseline"
    
    z_score = abs((value - mean) / std)
    is_anomaly = z_score > threshold
    
    if is_anomaly:
        description = f"⚠️ Unusual spike detected! ({z_score:.2f}σ from mean)"
    else:
        description = f"✓ Emission within normal range ({z_score:.2f}σ from mean)"
    
    return is_anomaly, z_score, description


def detect_user_anomalies(user):
    """Detect anomalies in user's emission history."""
    logs = EmissionLog.objects.filter(user=user).order_by('date')
    
    if logs.count() < 3:
        return {
            'has_anomalies': False,
            'anomalies': [],
            'total_checked': logs.count(),
            'message': 'Need at least 3 entries to detect anomalies'
        }
    
    emissions = [log.co2_emission for log in logs]
    anomalies = []
    
    for i, log in enumerate(logs):
        if i < 2:
            continue
        history = emissions[:i]
        is_anomaly, z_score, description = detect_anomaly(log.co2_emission, history)
        
        if is_anomaly:
            anomalies.append({
                'date': str(log.date),
                'emission': log.co2_emission,
                'z_score': round(z_score, 2),
                'description': description,
                'travel': log.km_travel,
                'electricity': log.electricity_units,
                'meals': log.meals_calories
            })
    
    return {
        'has_anomalies': len(anomalies) > 0,
        'anomalies': anomalies,
        'total_checked': logs.count(),
        'anomaly_count': len(anomalies),
        'anomaly_percentage': round((len(anomalies) / logs.count()) * 100, 1) if logs.count() > 0 else 0
    }


def get_anomaly_summary(user):
    """Get summary statistics about user's anomalies."""
    anomaly_data = detect_user_anomalies(user)
    
    if not anomaly_data['has_anomalies']:
        return {
            'status': '✓ No anomalies detected',
            'severity': 'none',
            'count': 0,
            'latest': None
        }
    
    anomalies = anomaly_data['anomalies']
    latest_anomaly = anomalies[-1] if anomalies else None
    max_z_score = max([a['z_score'] for a in anomalies])
    
    if max_z_score > 4:
        severity = 'critical'
        status = '🔴 Critical anomalies detected'
    elif max_z_score > 3:
        severity = 'high'
        status = '⚠️ High anomalies detected'
    else:
        severity = 'moderate'
        status = '🟡 Moderate anomalies detected'
    
    return {
        'status': status,
        'severity': severity,
        'count': len(anomalies),
        'latest': latest_anomaly,
        'max_z_score': max_z_score,
        'percentage': anomaly_data['anomaly_percentage']
    }


@login_required(login_url='login')
def dashboard(request):
    """
    Display user's personal dashboard with emissions data, tips, future predictions, and anomalies.
    Only accessible to logged-in users.
    """
    # Filter emissions by current logged-in user
    emissions = Emission.objects.filter(user=request.user).order_by('-date')
    latest = emissions.first()

    # Group emissions by date to get daily totals
    daily_emissions = Emission.objects.filter(user=request.user).annotate(
        date_only=TruncDate('created_at')
    ).values('date_only').annotate(
        total=Sum('total_co2')
    ).order_by('date_only')

    # Extract data for charts
    chart_dates = [str(emission['date_only']) for emission in daily_emissions]
    chart_co2_values = [float(emission['total']) for emission in daily_emissions]
    
    # Calculate metrics
    total_days_tracked = daily_emissions.count()
    average_daily_emission = sum(chart_co2_values) / total_days_tracked if total_days_tracked > 0 else 0

    # Get future predictions
    future_dates = []
    future_values = []
    healthy_range = []
    has_future_predictions = False
    
    try:
        user_metrics = get_user_average_metrics(user=request.user)
        future_predictions = predict_future_emissions(
            days_ahead=30,
            avg_travel=user_metrics['avg_travel'],
            avg_electricity=user_metrics['avg_electricity'],
            avg_fuel=user_metrics['avg_fuel']
        )

        # Prepare future prediction data for chart
        if future_predictions and future_predictions.get('dates'):
            future_dates = future_predictions['dates']
            future_values = future_predictions['predictions']
            # Create healthy range array for comparison (constant line)
            healthy_range = [HEALTHY_EMISSION_TARGET] * len(future_dates)
            has_future_predictions = True
    except Exception as e:
        print(f"Error getting future predictions: {e}")
        has_future_predictions = False

    # Calculate if future emissions are within healthy range
    avg_future_emission = sum(future_values) / len(future_values) if future_values else 0
    within_healthy_range = avg_future_emission <= HEALTHY_EMISSION_TARGET
    difference = avg_future_emission - HEALTHY_EMISSION_TARGET

    # Get anomaly detection data
    try:
        anomaly_summary = get_anomaly_summary(request.user)
        anomaly_details = detect_user_anomalies(request.user)
        
        # Prepare anomaly data for display
        anomaly_dates = []
        anomaly_values = []
        if anomaly_details['has_anomalies']:
            for anomaly in anomaly_details['anomalies']:
                anomaly_dates.append(anomaly['date'])
                anomaly_values.append(anomaly['emission'])
    except Exception as e:
        print(f"Error getting anomalies: {e}")
        anomaly_summary = {'status': '✓ No data', 'severity': 'none', 'count': 0}
        anomaly_details = {'has_anomalies': False, 'anomalies': []}
        anomaly_dates = []
        anomaly_values = []

    tips = []
    if latest:
        tips = generate_tips(latest.total_co2)

    return render(request, 'dashboard.html', {
        'latest': latest,
        'emissions': emissions,
        'tips': tips,
        'total_days_tracked': total_days_tracked,
        'average_daily_emission': f"{average_daily_emission:.2f}",
        'chart_dates': json.dumps(chart_dates),
        'chart_co2_values': json.dumps(chart_co2_values),
        'future_dates': json.dumps(future_dates),
        'future_predictions': json.dumps(future_values),
        'healthy_range': json.dumps(healthy_range),
        'has_future_predictions': has_future_predictions,
        'avg_future_emission': f"{avg_future_emission:.2f}",
        'within_healthy_range': within_healthy_range,
        'healthy_target': HEALTHY_EMISSION_TARGET,
        'emission_difference': f"{abs(difference):.2f}",
        # Anomaly data
        'anomaly_summary': anomaly_summary,
        'anomaly_details': anomaly_details,
        'anomaly_dates': json.dumps(anomaly_dates),
        'anomaly_values': json.dumps(anomaly_values),
    })
