from .models import Emission
from .services import calculate_total_emission

def save_emission(activity):
    total = calculate_total_emission(activity)

    Emission.objects.create(
        total_co2=total
    )
