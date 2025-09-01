from django.urls import path
from . import views
from . import role_views
from . import example_views

urlpatterns = [
    path('register/', views.register_user, name='user-register'),
    path('login/', views.login_user, name='user-login'),
    path('logout/', views.logout_user, name='user-logout'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='user-profile-update'),
    
    # Role management endpoints
    path('roles/', role_views.list_roles, name='list-roles'),
    path('roles/create/', role_views.create_role, name='create-role'),
    path('roles/<str:role_name>/delete/', role_views.delete_role, name='delete-role'),
    path('roles/assign/', role_views.assign_user_to_role, name='assign-user-to-role'),
    path('roles/remove/', role_views.remove_user_from_role, name='remove-user-from-role'),
    path('roles/user/<int:user_id>/', role_views.get_user_roles, name='get-user-roles'),
    
    # Permission management endpoints
    path('permissions/', role_views.list_permissions, name='list-permissions'),
    path('permissions/assign/', role_views.assign_permission_to_user, name='assign-permission-to-user'),
    path('permissions/check/<int:user_id>/<str:permission_codename>/', role_views.user_has_permission, name='user-has-permission'),
    
    # Example views demonstrating role management
    path('example/admin-dashboard/', example_views.admin_dashboard, name='admin-dashboard'),
    path('example/view-user-data/', example_views.view_user_data, name='view-user-data'),
    path('example/edit-user-data/', example_views.edit_user_data, name='edit-user-data'),
    path('example/assign-role/', example_views.assign_role_example, name='assign-role-example'),
]