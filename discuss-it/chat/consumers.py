# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.utils import timezone

from django.contrib.auth.models import User
import time

from core.models import ChatEntry, ChatRooms
#from core.forms import ChatEntryForm

#from request_middleware.middleware import get_request

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        if ChatRooms.objects.filter(name=self.room_name).exists():
            chatroom = ChatRooms.objects.get(name=self.room_name)
            if chatroom.user_number == 2:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "chat_message", "message": "User has joined", "username": "Admin"}
            )
            else:
                chatroom.user_number += 1

    def disconnect(self, close_code):
        # Leave room group
        if ChatRooms.objects.filter(name=self.room_name).exists():
            chatroom = ChatRooms.objects.get(name=self.room_name)

        #async_to_sync(self.channel_layer.group_send)(
        #    self.room_group_name, {"type": "chat_message", "message": "User has disconnected", "username": "Admin"}
        #)
            chatroom.user_number -= 1
            chatroom.save()
            if chatroom.user_number == 0:
                chatroom.delete()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["room_username"]
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message, "username": username}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = str(event['username'] + ": " + event["message"])
        chatroom = ChatRooms.objects.get(name=self.room_name)
        chat_message = ChatEntry()
        chat_message.entry = message
        chat_message.chatroom = chatroom
        chat_message.username = event['username']
        chat_message.timestamp = time.time()
        chat_message.save()
        for sent_item in ChatEntry.objects.filter(chatroom=chatroom):
            if ChatEntry.objects.filter(entry=sent_item.entry, timestamp=sent_item.timestamp).count()>1:
                sent_item.delete()
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
