import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import UpdateModelMixin,CreateModelMixin, DeleteModelMixin, ListModelMixin
from djangochannelsrestframework.observer import model_observer

from .models import Room, Message
from .serializers import MessageSerializer

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None

    def connect(self,**kwargs):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
        
        Message.objects.create(user=self.scope['user'], room=self.room, content=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))


class MessageConsumer(ListModelMixin, GenericAsyncAPIConsumer, CreateModelMixin):
    
    queryset=Message.objects.all()
    serializer_class=MessageSerializer
    

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        user = self.scope['user']
        return qs.filter(room__name=self.scope['url_route']['kwargs']['room_name'])

    async def connect(self, **kwargs):
        await super().connect()
        await self.model_change.subscribe()
        print("Connection is made")
        print(self.scope['user'])
        
        
    @model_observer(Message)
    async def model_change(self, message, observer=None ,**kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, request_id=None, **kwargs):
        print(dict(data=MessageSerializer(instance=instance).data, action=action.value))
        return dict(data=MessageSerializer(instance=instance).data, action=action.value)

    async def disconnect(self, message):
        print("Connection is over")
        await super().disconnect(message)

class MessageDeleteUpdateConsumer(GenericAsyncAPIConsumer, 
                      UpdateModelMixin, DeleteModelMixin):
    queryset=Message.objects.all()
    serializer_class=MessageSerializer
