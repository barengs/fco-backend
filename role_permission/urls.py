from django.urls import path
from . import views

urlpatterns = [
    # Role management endpoints
    path('roles/', views.list_roles, name='list-roles'),
    path('roles/create/', views.create_role, name='create-role'),
    path('roles/<str:role_name>/delete/', views.delete_role, name='delete-role'),
    path('roles/assign/', views.assign_user_to_role, name='assign-user-to-role'),
    path('roles/remove/', views.remove_user_from_role, name='remove-user-from-role'),
    path('roles/user/<int:user_id>/', views.get_user_roles, name='get-user-roles'),
    
    # Permission management endpoints
    path('permissions/', views.list_permissions, name='list-permissions'),
    path('permissions/assign/', views.assign_permission_to_user, name='assign-permission-to-user'),
    path('permissions/check/<int:user_id>/<str:permission_codename>/', views.user_has_permission, name='user-has-permission'),
]