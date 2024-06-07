import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import MessageInChat
from Activities.models import Course, Subscription
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope["url_route"]["kwargs"]["course_id"]
        self.user = self.scope["user"]
        self.room_group_name = "chat_%s" % self.course_id

        if await self.can_access_chat(self.user, self.course_id):
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            messages = await self.get_message_history()
            for message in messages:
                await self.send(text_data=json.dumps({
                    'username': message['author__username'],
                    'message': message['content'], 
                    'timestamp': message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json["username"]
        message = text_data_json["message"]

        await self.save_message(username, message)

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "username": username,
                "message": message,
                "timestamp": self.get_current_timestamp()
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        await self.send(text_data=json.dumps({"username": username, "message": message, "timestamp": timestamp}))

    @database_sync_to_async
    def get_message_history(self):
        messages = MessageInChat.objects.filter(course_id=self.course_id).order_by('timestamp')[:50]
        return list(messages.values('author__username', 'content', 'timestamp'))

    @database_sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        MessageInChat.objects.create(author=user, content=message, course_id=self.course_id)

    @database_sync_to_async
    def can_access_chat(self, user, course_id):
        if user.groups.filter(name="culture").exists():
            return True
        
        if user.groups.filter(name="administration").exists():
            return True
        
        return Subscription.objects.filter(user=user, course_id=course_id).exists()

    def get_current_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
