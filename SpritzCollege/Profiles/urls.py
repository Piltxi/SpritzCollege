from django.urls import path
from .views import *

urlpatterns = [
    path('manage/', ManageUserGroupsView.as_view(), name='manage_user_groups'),
    path('register/', register, name='register'),
    
    path('myprofile/', profile_edit, name='profile_edit'),
    path('edit-profile/', ProfileUpdateView.as_view, name='edit_profile'),
    
    path('messages/', MessageListView.as_view(), name='my_messages'),
    path('manage_membership/', manage_group_membership, name='manage_membership'),
    
    path('messages/da/', delete_all_messages, name='delete_messages'),
]