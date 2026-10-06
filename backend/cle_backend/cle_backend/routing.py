from django.urls import re_path
from cle_backend import consumers

websocket_urlpatterns = [
    re_path(r"ws/mi_canal/$", consumers.MiConsumer.as_asgi()),
]