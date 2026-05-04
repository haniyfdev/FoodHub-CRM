import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # JwtAuthMiddleware orqali foydalanuvchini olamiz
        self.user = self.scope.get("user")

        # Login qilmagan foydalanuvchini bloklaymiz
        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        # Foydalanuvchining restoran ID sini olamiz
        try:
            self.restaurant_id = self.user.profile.restaurant.id
            self.room_group_name = f'restaurant_{self.restaurant_id}_updates'

            # Guruhga qo'shilamiz
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept() # Aloqani ochamiz
        except Exception:
            await self.close()

    async def disconnect(self, close_code):
        # Ulanish uzilganda guruhdan chiqish
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Signal'dan kelgan xabarni tutib brauzerga yuborish
    async def send_order_update(self, event):
        await self.send(text_data=json.dumps(event['message']))