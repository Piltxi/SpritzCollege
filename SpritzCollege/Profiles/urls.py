from django.urls import path
from .views import *

urlpatterns = [
    path('manage_user_groups/', manage_user_groups, name='manage_user_groups'),
    path('register/', register, name='register'),
    path('myprofile/', profile_edit, name='profile_edit'),
    path('messages/', MessageListView.as_view(), name='messages'),
]
