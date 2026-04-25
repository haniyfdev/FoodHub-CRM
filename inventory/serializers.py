from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Waste
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# -- -- -- -- -- -- -- -- -- --
class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(
        queryset=Product.objects.all())]) # bir nom bilan 2ta product bo'lmasin
    class Meta:
        model  = Product
        fields = ['id', 'name', 'unit', 'quantity', 'price']

    # -- -- -- -- --
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Narx 0 dan baland bo'lsin")
        return value
    
    # -- -- -- -- --
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Miqdor 0 dan kichik bo'lishi mumkin emas")
        return value
    
    # -- -- -- -- --
    def validate(self, data):
        if data.get('unit') == 'dona' and data.get('quantity') % 1 != 0:
            raise serializers.ValidationError({"quantity": "Mahsulot soni butun son bo'lishi kerek"})
        return data
    
# -- -- -- -- -- -- -- -- -- --
class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Waste
        fields = ['id', 'menu_item', 'product', 'quantity', 'description', 
                  'reason', 'responsible_person', 'created_at']
        
    # -- -- -- -- --
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Miqdor 0 dan katta bo'lishi kerek")
        return value
    
