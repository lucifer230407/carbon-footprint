from django.shortcuts import render
from emissions.models import Emission
from emissions.services import generate_tips


def dashboard(request):
    emissions = Emission.objects.all().order_by('-date')
    latest = emissions.first()

    tips = []
    if latest:
        tips = generate_tips(latest.total_co2)

    return render(request, 'dashboard.html', {
        'latest': latest,
        'emissions': emissions,
        'tips': tips
    })

