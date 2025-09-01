from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='user-register'),
    path('login/', views.login_user, name='user-login'),
    path('logout/', views.logout_user, name='user-logout'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='user-profile-update'),
]