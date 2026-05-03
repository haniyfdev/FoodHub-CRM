from django.urls import re_path
from . import consumers

# Bu websocket protokoli

websocket_urlpatterns = [
    re_path(r'ws/orders/$', consumers.OrderConsumer.as_asgi()),
]






