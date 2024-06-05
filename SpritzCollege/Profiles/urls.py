from django.urls import path
from .views import *

urlpatterns = [
    path('manage/', ManageUserGroupsView.as_view(), name='manage_user_groups'),
    path('register/', register, name='register'),
    
    path('messages/', MessageListView.as_view(), name='my_messages'),
    path('manage_membership/', manage_group_membership, name='manage_membership'),
    
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('profile/delete/', UserDeleteView.as_view(), name='profile_delete'),
    path('profile/deleted/', TemplateView.as_view(template_name='Profiles/account_deleted.html'), name='account_deleted'),
    
    path('messages/da/', delete_all_messages, name='delete_messages'),
    
    path('course/<int:course_id>/chat/', course_chat, name='course_chat'),
    path('reset_course_chat/<int:course_id>/', reset_course_chat, name='reset_course_chat'),
    
    path('chat/<str:username>/', direct_chat, name='direct_chat'),
    path('personal_chats/', my_chats, name='personal_chats'),
]