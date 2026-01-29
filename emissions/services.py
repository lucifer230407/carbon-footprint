# emissions/services.py

# Simple emission factors (approx real-world values)

TRAVEL_CO2_PER_KM = 0.21
ELECTRICITY_CO2_PER_KWH = 0.82
MEAL_CO2 = 1.5
WASTE_CO2_PER_KG = 0.6

def calculate_total_emission(activity):
    travel = float(activity.travel_km) * TRAVEL_CO2_PER_KM
    electricity = float(activity.electricity_kwh) * ELECTRICITY_CO2_PER_KWH
    meals = int(activity.meals) * MEAL_CO2
    waste = float(activity.waste_kg) * WASTE_CO2_PER_KG

    total = travel + electricity + meals + waste

    return round(total, 2)

def generate_tips(total):
    tips = []

    if total > 20:
        tips.append("Use public transport or carpool more often")
        tips.append("Reduce electricity usage by switching off unused appliances")
    if total > 10:
        tips.append("Try more plant-based meals")
        tips.append("Reduce plastic and waste generation")
    if total <= 10:
        tips.append("Great job! Maintain your eco-friendly habits")

    return tips


    return round(total, 2)
