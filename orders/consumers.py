import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class OrderConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'boss_updates'
        # boss uchun maxsus kanal guruhi

        # Barcha kanallarni bir umumiy guruhga qo'shamiz
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # ulanishni rasman qabul qilamiz
        await self.accept() #handshake
        
# - - - - - - - - - - - - - - - 

    # 2.Mijoz brauzerni yopsa yoki ulanish uzilsa ishlaydi
    async def disconnect(self, code):
        # ulanish uzildimi, guruhdan o'chiramiz
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

# - - - - - - - - - - - - - - - 
    
    # 3.Bu metod guruhdan xabar kelganda uni tutuib oladi
    # signal orqali 'send_order_update' turi yuborilda shu ishga tushadi

    async def send_order_update(self, event):
        # Siganl yuborgan ma'lumotni (message)ni ajratib olamiz
        message = event['message']

        await self.send(text_data=json.dumps(message))
        
