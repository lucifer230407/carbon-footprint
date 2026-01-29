from django.urls import path
from .views import signup, user_login, user_logout, login_history

urlpatterns = [
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('history/', login_history, name='login_history'),
]
