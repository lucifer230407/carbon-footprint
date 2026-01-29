from django.contrib import admin
from .models import LoginHistory


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_type', 'login_time')
    list_filter = ('login_type', 'login_time')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('login_time',)
    ordering = ('-login_time',)
