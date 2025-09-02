from django.contrib import admin
from .models import Ship

@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_number', 'length', 'width', 'gross_tonnage', 'year_built', 'home_port', 'active')
    list_filter = ('active', 'year_built', 'home_port')
    search_fields = ('name', 'reg_number')
    ordering = ('name',)
