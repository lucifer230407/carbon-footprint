from django.urls import path
from .views import carbon_input, anomaly_check

urlpatterns = [
    path("", carbon_input, name="carbon_input"),
    path("anomaly-check/", anomaly_check, name="anomaly_check"),
]
