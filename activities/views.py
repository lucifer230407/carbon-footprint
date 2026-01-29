from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Activity
from emissions.models import Emission, EmissionLog
from emissions.ml_model import predict_carbon
from emissions.services import generate_tips
from datetime import datetime


@login_required(login_url='login')
def add_activity(request):
    """
    Handle activity creation and ML-based carbon emission prediction.
    Uses ML model to predict emissions and saves to database with tips.
    Only accessible to logged-in users.
    Supports custom date input for logging past activities.
    Saves to both Emission and EmissionLog models.
    """
    error = None
    
    if request.method == "POST":
        try:
            travel_km = float(request.POST.get('travel_km', 0))
            electricity_kwh = float(request.POST.get('electricity_kwh', 0))
            meals = float(request.POST.get('meals', 0))
            waste_kg = float(request.POST.get('waste_kg', 0))
            activity_date = request.POST.get('activity_date')

            # Check if all values are zero
            if travel_km == 0 and electricity_kwh == 0 and meals == 0 and waste_kg == 0:
                error = "Please enter at least one value to log your activity"
                return render(request, 'input.html', {'error': error})

            # Parse custom date if provided, otherwise use today's date
            if activity_date:
                try:
                    activity_date = datetime.strptime(activity_date, '%Y-%m-%d').date()
                except ValueError:
                    error = "Invalid date format. Please use YYYY-MM-DD"
                    return render(request, 'input.html', {'error': error})
            else:
                activity_date = datetime.now().date()

            # Create activity record with current user and custom date
            activity = Activity.objects.create(
                user=request.user,
                travel_km=travel_km,
                electricity_kwh=electricity_kwh,
                meals=meals,
                waste_kg=waste_kg,
                date=activity_date
            )

            # ML Model prediction
            predicted_emission = round(predict_carbon(travel_km, electricity_kwh, meals, waste_kg), 2)

            # Save emission with user tracking and custom date
            Emission.objects.create(
                user=request.user,
                total_co2=predicted_emission,
                date=activity_date
            )

            # Save comprehensive log to EmissionLog table
            EmissionLog.objects.create(
                user=request.user,
                date=activity_date,
                km_travel=travel_km,
                electricity_units=electricity_kwh,
                meals_calories=int(meals),
                co2_emission=predicted_emission
            )

            return redirect('dashboard')
        except (ValueError, TypeError):
            error = 'Please enter valid numbers'
            return render(request, 'input.html', {'error': error})

    return render(request, 'input.html')
