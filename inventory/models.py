from django.db import models
from users.models import RestaurantModel, Profile
from orders.models import MenuItem
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Product

# -- -- -- -- -- -- -- -- -- -- 
class Product(RestaurantModel):
    class Unit(models.TextChoices):
        KG   = 'kg', 'kg'
        LITR = 'litr', 'litr'
        DONA = 'dona', 'dona'

    name     = models.CharField(max_length=100)
    unit     = models.CharField(max_length=50, choices=Unit.choices, default=Unit.KG)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price    = models.DecimalField(validators=[MinValueValidator(100)], max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name
    
# -- -- -- -- -- -- -- -- -- -- 
class Waste(RestaurantModel):
    class Reason(models.TextChoices):
        EXPIRED   = 'expired', "muddati o'tdi"
        SPOILED   = 'spoiled', 'saqlay olinmadi'
        MISTAKE   = 'mistake', 'xato tayyorlandi'
        BROKEN    = 'broken', 'sindirildi'
        DROPPED   = 'dropped', "to'kildi"
        LEFTOVERS = 'leftovers', 'ortib qoldi'
        ANOTHER   = 'another', 'boshqa sabab'

    menu_item          = models.ForeignKey(MenuItem, on_delete=models.PROTECT, 
                                    related_name='wastes', null=True, blank=True)
    product            = models.ForeignKey(Product, on_delete=models.PROTECT,
                                    related_name='wastes', null=True, blank=True)
    
    quantity           = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description        = models.TextField(blank=True, null=True)
    reason             = models.CharField(max_length=50, choices=Reason.choices)
    responsible_person = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='guilty')
    created_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        item = self.menu_item.name if self.menu_item else self.product.name
        return f"{item} - {self.reason}"
    
# -- -- -- -- -- -- -- -- -- -- 
@receiver(post_save, sender=Product)
def check_stock(sender, instance, **kwargs):
    if instance.quantity < 10:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'boss_updates', # biz ochgan guruh
            {
                'type': 'send_order_update',
                'message': {
                    'event': 'inventory_warning',
                    'product_name': instance.name,
                    'quantity': instance.quantity,
                    'unit': instance.unit,
                    'status': f"Diqqat! {instance.name} tugayapti ⚠️"
                }
            }
        )









