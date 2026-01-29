from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Activity
from emissions.models import Emission
from emissions.ml_model import predict_carbon
from emissions.services import generate_tips


@login_required(login_url='login')
def add_activity(request):
    """
    Handle activity creation and ML-based carbon emission prediction.
    Uses ML model to predict emissions and saves to database with tips.
    Only accessible to logged-in users.
    """
    error = None
    
    if request.method == "POST":
        try:
            travel_km = float(request.POST.get('travel_km', 0))
            electricity_kwh = float(request.POST.get('electricity_kwh', 0))
            meals = float(request.POST.get('meals', 0))
            waste_kg = float(request.POST.get('waste_kg', 0))

            # Check if all values are zero
            if travel_km == 0 and electricity_kwh == 0 and meals == 0 and waste_kg == 0:
                error = "Please enter at least one value to log your activity"
                return render(request, 'input.html', {'error': error})

            # Create activity record with current user
            activity = Activity.objects.create(
                user=request.user,
                travel_km=travel_km,
                electricity_kwh=electricity_kwh,
                meals=meals,
                waste_kg=waste_kg
            )

            # ML Model prediction
            predicted_emission = round(predict_carbon(travel_km, electricity_kwh, meals, waste_kg), 2)

            # Save emission with user tracking
            Emission.objects.create(
                user=request.user,
                total_co2=predicted_emission
            )

            return redirect('dashboard')
        except (ValueError, TypeError):
            error = 'Please enter valid numbers'
            return render(request, 'input.html', {'error': error})

    return render(request, 'input.html')
