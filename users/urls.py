from django.urls import path
from . import views
from . import example_views

urlpatterns = [
    path('register/', views.register_user, name='user-register'),
    path('login/', views.login_user, name='user-login'),
    path('logout/', views.logout_user, name='user-logout'),
    path('token/refresh/', views.token_refresh, name='token-refresh'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='user-profile-update'),
    path('profile/ship-owner/update/', views.update_ship_owner_profile, name='ship-owner-profile-update'),
    path('profile/captain/update/', views.update_captain_profile, name='captain-profile-update'),
    path('profile/admin/update/', views.update_admin_profile, name='admin-profile-update'),
    
    # Example views demonstrating role management
    path('example/admin-dashboard/', example_views.admin_dashboard, name='admin-dashboard'),
    path('example/view-user-data/', example_views.view_user_data, name='view-user-data'),
    path('example/edit-user-data/', example_views.edit_user_data, name='edit-user-data'),
    path('example/assign-role/', example_views.assign_role_example, name='assign-role-example'),
]