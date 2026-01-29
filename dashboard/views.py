from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from emissions.models import Emission
from emissions.services import generate_tips


@login_required(login_url='login')
def dashboard(request):
    """
    Display user's personal dashboard with emissions data and tips.
    Only accessible to logged-in users.
    """
    # Filter emissions by current logged-in user
    emissions = Emission.objects.filter(user=request.user).order_by('-date')
    latest = emissions.first()

    tips = []
    if latest:
        tips = generate_tips(latest.total_co2)

    return render(request, 'dashboard.html', {
        'latest': latest,
        'emissions': emissions,
        'tips': tips
    })

