from django.shortcuts import render, redirect

from .models import Activity
from emissions.views import save_emission


def add_activity(request):
    if request.method == "POST":
        travel_km = float(request.POST['travel_km'])
        electricity_kwh = float(request.POST['electricity_kwh'])
        meals = int(request.POST['meals'])
        waste_kg = float(request.POST['waste_kg'])

        activity = Activity.objects.create(

            travel_km=travel_km,
            electricity_kwh=electricity_kwh,
            meals=meals,
            waste_kg=waste_kg
        )

        save_emission(activity)

        return redirect('dashboard')

    return render(request, 'input.html')
