from django.urls import path
from .views import add_activity

urlpatterns = [
    path('add/', add_activity, name='add_activity'),
]
