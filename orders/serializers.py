from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, MenuItem, Order, OrderItem, Transaction
from rest_framework.validators import UniqueValidator

# -- -- -- -- -- -- -- -- -- --
class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model  = Category
        fields = ['id', 'name', 'label_num', 'is_active', 'product_count'] 
        read_only_fields = ['label_num']

# -- -- -- -- -- -- -- -- -- --
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = MenuItem
        fields = ['id', 'name', 'category', 'price', 'image', 'is_active']

    # -- -- -- -- --
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Narx 0 dan baland bo'lsin")
        return value 
    
# -- -- -- -- -- -- -- -- -- --
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.ReadOnlyField(source='menu_item.name')
    class Meta:
        model  = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'price']

# -- -- -- -- -- -- -- -- -- --  
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='order_items')
    class Meta:
        model  = Order
        fields = ['id', 'unique_num', 'cashier', 'shift', 'total_price', 'items', 'created_at']

# -- -- -- -- -- -- -- -- -- --
class TransactionSerializer(serializers.ModelSerializer):
    order_num = serializers.ReadOnlyField(source='order.unique_num')
    class Meta:
        model  = Transaction
        fields = ['id', 'order', 'order_num', 'payment_type', 'amount', 'paid_at'] 

