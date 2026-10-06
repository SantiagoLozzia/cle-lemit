import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import cle_backend.routing  # Este es tu archivo de rutas para WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cle_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Para las peticiones HTTP tradicionales
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                cle_backend.routing.websocket_urlpatterns
            )
        )
    ),
})
