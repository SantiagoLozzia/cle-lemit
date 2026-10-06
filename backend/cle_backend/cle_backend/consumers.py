# cle_backend/consumers.py
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


@database_sync_to_async
def get_user_from_token(raw_token):
    authentication = JWTAuthentication()
    token = authentication.get_validated_token(raw_token.encode('ascii'))
    return authentication.get_user(token)

class MiConsumer(AsyncWebsocketConsumer):
    """
    Un solo consumer que agrupa a todos los clientes en 'aranceles'.
    Después podrás reutilizar el mismo patrón (otro grupo) para
    notificaciones de otros módulos/menu.
    """

    # ──────────────────────────── Conexión ────────────────────────────
    async def connect(self):
        subprotocols = self.scope.get('subprotocols', [])
        if len(subprotocols) != 2 or subprotocols[0] != 'jwt':
            await self.close(code=4401)
            return

        try:
            self.scope['user'] = await get_user_from_token(subprotocols[1])
        except (AuthenticationFailed, UnicodeEncodeError):
            await self.close(code=4401)
            return

        # 1) Añade al usuario al grupo
        await self.channel_layer.group_add("aranceles", self.channel_name)
        # 2) Acepta la conexión
        await self.accept(subprotocol='jwt')
        # 3) Mensaje inicial
        await self.send_json({"message": "Conexión WebSocket establecida"})

    async def disconnect(self, close_code):
        # Saca al usuario del grupo al desconectarse
        await self.channel_layer.group_discard("aranceles", self.channel_name)

    # ──────────────────────────── Entrante desde el cliente ──────────
    async def receive(self, text_data):
        """
        Si quisieras procesar mensajes que mande el navegador,
        aquí los manejarías.  Por ahora solo los devolvemos.
        """
        try:
            data = json.loads(text_data)
            await self.send_json({"echo": data})
        except json.JSONDecodeError:
            await self.send_json({"error": "JSON inválido"})

    # ──────────────────────────── Entrante desde el servidor ─────────
    # Este método se llama cuando el back-end hace:
    #   group_send("aranceles", {"type": "nuevo_servicio", ...})
    async def nuevo_servicio(self, event):
        """
        Broadcast automático a todos los clientes del grupo.
        event["servicio"] debe venir serializado (dict JSON-serializable).
        """
        await self.send_json({
            "aranceles_action": "add",
            "servicio": event["servicio"],
        })

    # Helper para no repetir json.dumps
    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))
