# emissions/services.py

def generate_tips(total):
    """
    Generate personalized carbon reduction tips based on total emission.
    
    Args:
        total (float): Total CO2 emission in kg
    
    Returns:
        list: List of personalized tips
    """
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
