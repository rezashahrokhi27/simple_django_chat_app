import asyncio
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name
#         print(self.room_name,self.room_group_name)
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )
#
#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))
#
# import json
#
# from channels.generic.websocket import AsyncWebsocketConsumer
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name
#
#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))
#



import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

from .serializers import MessageSerializer
from .models import Message, Chat
from rest_framework.renderers import JSONRenderer


user = get_user_model()
class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        message = data["message"]
        author = data['username']
        roomname = data['roomname']
        related_chat = Chat.objects.get(roomname=roomname)
        user_model = user.objects.filter(username=author).first()
        message_model = Message.objects.create(author=user_model, content=message, related_chat=related_chat)
        result = eval(self.message_serializer(message_model))
        # result = eval(result)['content']
        self.send_to_chat_message(result)

    def fetch_message(self, data):
        roomname = data['roomname']
        qs = Message.last_message(self, roomname)
        message_jason = self.message_serializer(qs)
        content = {
            'message': eval(message_jason),
            "command": "fetch_message"
        }
        self.chat_message(content)


    def message_serializer(self, qs):
        print((lambda qs : True if (qs.__class__.__name__ == 'QuerySet') else False)(qs))
        serialized = MessageSerializer(qs, many=(lambda qs : True if (qs.__class__.__name__ == 'QuerySet') else False)(qs))
        content = JSONRenderer().render(serialized.data)
        return content


    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    commands ={
        'new_message':new_message,
        'fetch_message':fetch_message,
    }

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", None)
        username = text_data_json.get('username', None)
        print(username)
        command = text_data_json["command"]

        self.commands[command](self, text_data_json)

    def send_to_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "content":message['content'],
                "command": "new_message",
                '__str__': message['__str__']
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))