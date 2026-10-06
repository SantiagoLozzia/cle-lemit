# cle_backend/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MiConsumer(AsyncWebsocketConsumer):
    """
    Un solo consumer que agrupa a todos los clientes en 'aranceles'.
    Después podrás reutilizar el mismo patrón (otro grupo) para
    notificaciones de otros módulos/menu.
    """

    # ──────────────────────────── Conexión ────────────────────────────
    async def connect(self):
        # 1) Añade al usuario al grupo
        await self.channel_layer.group_add("aranceles", self.channel_name)
        # 2) Acepta la conexión
        await self.accept()
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
