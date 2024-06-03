from django.contrib import admin

from .models import Profile, Message

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date', 'profile_pic')
    search_fields = ('user__username', 'location', 'bio')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'timestamp', 'read')
    search_fields = ('user__username', 'title', 'content')
    list_filter = ('read', 'timestamp')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
