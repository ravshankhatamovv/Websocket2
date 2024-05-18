from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/message/$', consumers.MessageConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/del-upd/$', consumers.MessageDeleteUpdateConsumer.as_asgi()),
]