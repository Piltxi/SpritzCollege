from django.db.models.signals import post_save
from django.dispatch import receiver
from Activities.models import Event
from .models import Message
from django.contrib.auth.models import User

@receiver(post_save, sender=Event)
def create_event_notification(sender, instance, created, **kwargs):
    if created:
        print("Sta succedendo qualcosa")
        title = f"New Event Created: {instance.name}"
        content = f"A new event has been created:\n\nName: {instance.name}\nDescription: {instance.description}\nDate: {instance.date}\n\nDon't miss it!"
        users = User.objects.all()
        for user in users:
            Message.objects.create(user=user, title=title, content=content)