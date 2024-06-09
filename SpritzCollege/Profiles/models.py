from django.db import models
from django.contrib.auth.models import User
from Activities.models import Course
from SpritzCollege import settings

import os
import glob

def path_profile_pic(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.user.id}.{ext}'
    directory = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
    filepath = os.path.join(directory, filename)
 
    possibly_old_files = glob.glob(os.path.join(directory, f'{instance.user.id}.*'))
    for old_file in possibly_old_files:
        if os.path.isfile(old_file):
            os.remove(old_file)
    
    return os.path.join('profile_pics', filename)

class Profile(models.Model):
    CATEGORY_CHOICES = [
        ('ANY', 'uncategorized'),
        ('TCH', 'tech course'),
        ('LTR', 'literature course'),
        ('LAN', 'language course'),
        ('HND', 'craftsman course'),
        ('ART', 'art course'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to=path_profile_pic, default='user.png')
    interests = models.TextField(blank=True)
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.user.username} - {self.title}"
    
class MessageInChat (models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"{self.author.username}: {self.content}"
    
class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.content[:20]}"