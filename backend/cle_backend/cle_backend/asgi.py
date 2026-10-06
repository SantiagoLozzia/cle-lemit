import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import cle_backend.routing  # Este es tu archivo de rutas para WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cle_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Para las peticiones HTTP tradicionales
    "websocket": AuthMiddlewareStack(  # Para las conexiones WebSocket
        URLRouter(
            cle_backend.routing.websocket_urlpatterns  # Las rutas de WebSocket definidas en routing.py
        )
    ),
})
