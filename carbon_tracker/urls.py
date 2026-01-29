from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='dashboard/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('activity/', include('activities.urls')),
    path('dashboard/', include('dashboard.urls')),
    path("emissions/", include("emissions.urls")),
    path("chatbot/", include("chatbot.urls")),
]
