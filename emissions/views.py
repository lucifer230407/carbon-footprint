from django.http import JsonResponse
from django.shortcuts import render

from .models import Emission
from .ml_model import predict_carbon
from .services import generate_tips

def carbon_input(request):
    """
    Handle user carbon input and real-time ML-based prediction.
    Saves prediction to database and generates personalized tips.
    """
    result = None
    tips = []

    if request.method == "POST":
        try:
            distance = float(request.POST.get("travel_km", 0))
            electricity = float(request.POST.get("electricity_kwh", 0))
            calories = float(request.POST.get("meals", 0))
            waste = float(request.POST.get("waste_kg", 0))

            # ML Model prediction
            result = round(predict_carbon(distance, electricity, calories, waste), 2)
            
            # Save to database (user is optional)
            user = request.user if request.user.is_authenticated else None
            Emission.objects.create(
                user=user,
                total_co2=result
            )
            
            # Generate tips based on prediction
            tips = generate_tips(result)
            
        except (ValueError, TypeError) as e:
            result = None
            tips = ["Please enter valid numbers"]

    return render(request, "input.html", {
        "result": result,
        "tips": tips
    })
