from django.db import models
from users.models import RestaurantModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = get_user_model()

# -- -- -- -- -- -- -- -- -- -- 
class Category(RestaurantModel):
    name       = models.CharField(max_length=60)
    label_num = models.IntegerField()
    is_active  = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.label_num:
            # agar lebel_num yo'q bo'lsa shu restaran'ni o'zini filterla va eng katta
            # sonni yani eng oxirgi sonni ol
            last_num = Category.objects.filter( 
               restaurant=self.restaurant).order_by('-label_num').first()
            self.label_num = (last_num.label_num + 1) if last_num else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.label_num}"

# -- -- -- -- -- -- -- -- -- -- 
class MenuItem(RestaurantModel):
    name      = models.CharField(max_length=150)
    category  = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    price     = models.DecimalField(validators=[MinValueValidator(1000)], max_digits=9, decimal_places=2)
    image     = models.ImageField(upload_to='images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# -- -- -- -- -- -- -- -- -- -- 
class Order(RestaurantModel):
    unique_num = models.IntegerField()
    cashier    = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    shift      = models.ForeignKey('staff.Shift', on_delete=models.PROTECT, related_name='orders')
    total_price = models.DecimalField(validators=[MinValueValidator(1000)], max_digits=9, decimal_places=2, default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_num:
            # agar lebel_num yo'q bo'lsa shu restaran'ni o'zini filterla va eng katta
            # sonni yani eng oxirgi sonni ol
            last_num = Order.objects.filter( 
               restaurant=self.restaurant).order_by('-unique_num').first()
            self.unique_num = (last_num.unique_num + 1) if last_num else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unique_num} - sonli buyurtma"
    
# -- -- -- -- -- -- -- -- -- -- 
class OrderItem(RestaurantModel): # bu orderni ichida bo'ladi nested
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name='menu_item')
    quantity  = models.IntegerField(default=0)
    price     = models.DecimalField(validators=[MinValueValidator(1000)], max_digits=9, decimal_places=2)

    def __str__(self):
        return self.menu_item.name

# -- -- -- -- -- -- -- -- -- -- 
class Transaction(RestaurantModel):
    class PaymentType(models.TextChoices):
        CARD = 'card', 'Karta'
        CASH = 'cash', 'Naqd'

    order        = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='transaction')
    payment_type = models.CharField(max_length=50, choices=PaymentType.choices, default=PaymentType.CASH)
    amount       = models.DecimalField(validators=[MinValueValidator(1000)], max_digits=9, decimal_places=2)
    paid_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_type} - {self.amount}"
    
# -- -- -- -- -- -- -- -- -- --
@receiver(post_save, sender=Order)
def notify_boss(sender, instance, created, **kwargs):
    if created: # if true bo'lsa demak update emas created ekan
        channel_layer = get_channel_layer() # redis bilan connect
        # signal async bo'lmagani uchun kerek
        async_to_sync(channel_layer.group_send)(
            'boss_updates', #qaysi guruhga ?
            {
                "type": "send_order_update",
                "message": {
                    # boss'ga boradigan ma'lumotlar
                    'event': 'new_order',
                    'order_id': instance.id,
                    'total_price': str(instance.total_price),
                    'status': 'Yangi buyurtma keldi'
                }
            }
        )


