# chat/consumers.py

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

        if await self.is_user_subscribed(self.user, self.course_id):
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            # Send message history
            messages = await self.get_message_history()
            for message in messages:
                await self.send(text_data=json.dumps({
                    'username': message['author__username'],  # Usa 'author__username' per accedere al nome utente
                    'message': message['content'],            # Usa 'content' per il contenuto del messaggio
                    'timestamp': message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                }))
        else:
            # Close the connection if the user is not subscribed to the course
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json["username"]
        message = text_data_json["message"]

        # Save message to database
        await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "username": username,
                "message": message,
                "timestamp": self.get_current_timestamp()
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"username": username, "message": message, "timestamp": timestamp}))

    @database_sync_to_async
    def get_message_history(self):
        messages = MessageInChat.objects.filter(course_id=self.course_id).order_by('-timestamp')[:50]
        return list(messages.values('author__username', 'content', 'timestamp'))

    @database_sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        MessageInChat.objects.create(author=user, content=message, course_id=self.course_id)

    @database_sync_to_async
    def is_user_subscribed(self, user, course_id):
        return Subscription.objects.filter(user=user, course_id=course_id).exists()

    def get_current_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
