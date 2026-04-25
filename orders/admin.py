from django.contrib import admin
from .models import Category, Order, OrderItem, MenuItem, Transaction
from . import views

class OrderItemInline(admin.TabularInline):
    """OrderItem Order ichida ko'rinib turishi uchun"""
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

# -- -- -- -- -- -- -- -- -- --
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'label_num', 'is_active')
    search_fields = ('name',)
    list_filter   = ('is_active',)


# -- -- -- -- -- -- -- -- -- -- 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('unique_num', 'cashier', 'shift', 'total_price', 'created_at')
    search_fields = ('unique_num',)
    list_filter   = ('cashier', 'shift')
    # inlines       = [OrderItemInline]


# -- -- -- -- -- -- -- -- -- -- 
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'price', 'image', 'is_active')
    search_fields = ('name', 'price')
    list_filter   = ('category', 'is_active')


# -- -- -- -- -- -- -- -- -- -- 
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display  = ('order', 'payment_type', 'amount', 'paid_at')
    search_fields = ('amount',)
    list_filter   = ('payment_type',)


