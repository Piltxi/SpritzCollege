from django.urls import path
from . import views

urlpatterns = [
    path('manage_user_groups/', views.manage_user_groups, name='manage_user_groups'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
