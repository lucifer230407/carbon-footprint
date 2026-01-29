from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .ml_model import predict_carbon
from .services import generate_tips
from dashboard.views import detect_user_anomalies, get_anomaly_summary

def carbon_input(request):
    """
    Handle user carbon input and real-time ML-based prediction.
    This is for PREDICTION ONLY - does NOT save to database.
    Data is only saved through the Log Activity feature.
    """
    result = None
    tips = []
    error = None

    if request.method == "POST":
        try:
            distance = float(request.POST.get("travel_km", 0))
            electricity = float(request.POST.get("electricity_kwh", 0))
            calories = float(request.POST.get("meals", 0))
            waste = float(request.POST.get("waste_kg", 0))

            # Check if all values are zero
            if distance == 0 and electricity == 0 and calories == 0 and waste == 0:
                error = "Please enter at least one value to calculate your carbon footprint"
            else:
                # ML Model prediction (NO DATABASE STORAGE)
                result = round(predict_carbon(distance, electricity, calories, waste), 2)
                
                # Generate tips based on prediction
                tips = generate_tips(result)
            
        except (ValueError, TypeError) as e:
            result = None
            tips = []
            error = "Please enter valid numbers"

    return render(request, "input.html", {
        "result": result,
        "tips": tips,
        "error": error
    })


@login_required(login_url='login')
def anomaly_check(request):
    """
    API endpoint to check for anomalies in user's emissions
    """
    anomaly_data = detect_user_anomalies(request.user)
    summary = get_anomaly_summary(request.user)
    
    return JsonResponse({
        'summary': summary,
        'details': anomaly_data
    })
