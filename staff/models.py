from django.db import models
from django.conf import settings 
from users.models import RestaurantModel
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

# -- -- -- -- -- -- -- -- -- --
class Shift(RestaurantModel):
    cashier      = models.ForeignKey(User, on_delete=models.PROTECT, related_name='shifts')
    opened_at    = models.DateTimeField(auto_now_add=True)
    closed_at    = models.DateTimeField(null=True, blank=True) # view'da qilamiz
    opening_cash = models.DecimalField(validators=[MinValueValidator(1000)], max_digits=15, decimal_places=2)
    closing_cash = models.DecimalField(validators=[MinValueValidator(1000)], max_digits=15, decimal_places=2, null=True, blank=True) # view'da qilamiz
    is_active    = models.BooleanField(default=True)

    def __str__(self):
        return f"Shift - {self.cashier.username}"

# -- -- -- -- -- -- -- -- -- --
class OrderAuditLog(RestaurantModel):
    class Action(models.TextChoices):
        CREATED   = 'created', 'Created'
        UPDATED   = 'updated', 'Updated'
        CANCELLED = 'cancelled', 'Cancelled'

    order       = models.ForeignKey('orders.Order', on_delete=models.PROTECT, related_name='audit_logs')
    old_data    = models.JSONField(null=True, blank=True)
    new_data    = models.JSONField()
    situation   = models.CharField(max_length=50, choices=Action.choices, default=Action.CREATED)
    description = models.TextField(null=True, blank=True)
    editor      = models.ForeignKey(User, on_delete=models.PROTECT, related_name='editor')

    def __str__(self):
        return f"{self.editor.username}"
    
# -- -- -- -- -- -- -- -- -- --
class EmployeeKPI(RestaurantModel):
    user      = models.OneToOneField(User, on_delete=models.PROTECT, related_name='employe_kpi')
    bonus_kpi = models.DecimalField(validators=[MinValueValidator(1000)], max_digits=15, decimal_places=2)
    salary    = models.DecimalField(validators=[MinValueValidator(100000)], max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} KPI {self.bonus_kpi}"
    

