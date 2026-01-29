from django.urls import path
from .views import carbon_input

urlpatterns = [
    path("", carbon_input, name="carbon_input"),
]
