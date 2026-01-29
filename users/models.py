from django.db import models
from django.contrib.auth.models import User

class LoginHistory(models.Model):
    """Track user login and signup activities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_time = models.DateTimeField(auto_now_add=True)
    login_type = models.CharField(max_length=10, choices=[('login', 'Login'), ('signup', 'Signup')], default='login')
    
    class Meta:
        ordering = ['-login_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.login_type} at {self.login_time}"
