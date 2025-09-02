from django.contrib import admin
from .models import FishSpecies, Fish

@admin.register(FishSpecies)
class FishSpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'scientific_name')
    ordering = ('name',)

@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'created_at')
    list_filter = ('species', 'created_at')
    search_fields = ('name', 'species__name')
    ordering = ('name',)