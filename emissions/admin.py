from django.contrib import admin
from .models import Emission, EmissionLog

@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_co2', 'date', 'created_at')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

@admin.register(EmissionLog)
class EmissionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'km_travel', 'electricity_units', 'meals_calories', 'co2_emission')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('User & Date', {'fields': ('user', 'date')}),
        ('Activity Details', {'fields': ('km_travel', 'electricity_units', 'meals_calories')}),
        ('Carbon Emissions', {'fields': ('co2_emission',)}),
        ('Metadata', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
