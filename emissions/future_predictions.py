import pickle
import os
from datetime import datetime, timedelta
import json
from django.db import models
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'future_emission_model.pkl')


def load_model():
    """Load the pre-trained future emission prediction model"""
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        return model
    except (FileNotFoundError, pickle.UnpicklingError, RuntimeError) as e:
        print(f"Warning: Could not load model from {MODEL_PATH}: {e}")
        print("Using fallback prediction based on historical data")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def predict_future_emissions(days_ahead=30, avg_travel=0, avg_electricity=0, avg_fuel=0):
    """
    Predict future CO2 emissions for the next N days
    
    Args:
        days_ahead: Number of days to predict (default 30)
        avg_travel: Average daily travel in km
        avg_electricity: Average daily electricity in kWh
        avg_fuel: Average daily fuel consumption
    
    Returns:
        Dictionary with predictions for each day
    """
    model = load_model()
    
    predictions = {}
    future_dates = []
    future_values = []
    
    today = datetime.now().date()
    
    try:
        # Calculate base emission from average values
        # Rough estimation: 0.12 kg CO2 per km, 0.4 kg CO2 per kWh, 0.001 kg per calorie
        base_emission = (avg_travel * 0.12) + (avg_electricity * 0.4) + (avg_fuel * 10)
        
        # Add some variance for natural fluctuations
        for day_offset in range(1, days_ahead + 1):
            future_date = today + timedelta(days=day_offset)
            
            if model:
                try:
                    day_of_year = future_date.timetuple().tm_yday
                    # Prepare features: [day_of_year, travel, electricity, fuel]
                    features = [[day_of_year, avg_travel, avg_electricity, avg_fuel]]
                    # Make prediction
                    prediction = float(model.predict(features)[0])
                except:
                    # Fallback to simple calculation
                    # Add seasonal variance (±20% based on day of year)
                    seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * day_offset / 365)
                    prediction = base_emission * seasonal_factor
            else:
                # Use simple historical average with slight variance
                seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * day_offset / 365)
                prediction = max(0.1, base_emission * seasonal_factor)
            
            predictions[str(future_date)] = float(prediction)
            future_dates.append(str(future_date))
            future_values.append(float(prediction))
    
    except Exception as e:
        print(f"Error making predictions: {e}")
        return None
    
    if not future_dates:
        return None
    
    return {
        'dates': future_dates,
        'predictions': future_values,
        'raw_predictions': predictions
    }


def get_user_average_metrics(user):
    """
    Calculate user's average metrics from their emission logs
    """
    from .models import EmissionLog
    
    logs = EmissionLog.objects.filter(user=user)
    
    if not logs.exists():
        return {
            'avg_travel': 0,
            'avg_electricity': 0,
            'avg_fuel': 0
        }
    
    total_travel = logs.aggregate(sum=models.Sum('km_travel'))['sum'] or 0
    total_electricity = logs.aggregate(sum=models.Sum('electricity_units'))['sum'] or 0
    count = logs.count()
    
    return {
        'avg_travel': total_travel / count if count > 0 else 0,
        'avg_electricity': total_electricity / count if count > 0 else 0,
        'avg_fuel': 0  # Not tracked in EmissionLog currently
    }
