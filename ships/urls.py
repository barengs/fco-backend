from django.urls import path
from . import views

app_name = 'ships'

urlpatterns = [
    path('', views.ShipListCreateView.as_view(), name='ship-list-create'),
    path('<int:pk>/', views.ShipRetrieveUpdateDestroyView.as_view(), name='ship-detail'),
    path('import/', views.ShipImportView.as_view(), name='ship-import'),
    path('template/', views.download_ship_template, name='ship-template'),
]