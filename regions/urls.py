from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_fishing_areas, name='list-fishing-areas'),
    path('<int:area_id>/', views.get_fishing_area, name='get-fishing-area'),
    path('create/', views.create_fishing_area, name='create-fishing-area'),
    path('<int:area_id>/update/', views.update_fishing_area, name='update-fishing-area'),
    path('<int:area_id>/delete/', views.delete_fishing_area, name='delete-fishing-area'),
    path('import/', views.import_fishing_areas, name='import-fishing-areas'),
    path('download-template/', views.download_import_template, name='download-fishing-area-template'),
]