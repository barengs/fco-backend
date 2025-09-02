from django.urls import path
from . import views

app_name = 'fishs'

urlpatterns = [
    # Fish Species URLs
    path('species/', views.FishSpeciesListCreateView.as_view(), name='species-list-create'),
    path('species/<int:pk>/', views.FishSpeciesRetrieveUpdateDestroyView.as_view(), name='species-detail'),
    path('species/import/', views.FishSpeciesImportView.as_view(), name='species-import'),
    path('species/template/', views.download_fish_species_template, name='species-template'),
    
    # Fish URLs
    path('fish/', views.FishListCreateView.as_view(), name='fish-list-create'),
    path('fish/<int:pk>/', views.FishRetrieveUpdateDestroyView.as_view(), name='fish-detail'),
    path('fish/import/', views.FishImportView.as_view(), name='fish-import'),
    path('fish/template/', views.download_fish_template, name='fish-template'),
]