from rest_framework import serializers
from .models import Shift, OrderAuditLog, EmployeeKPI

# -- -- -- -- -- -- -- -- -- --
class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Shift
        fields = ['cashier', 'opened_at', 'closed_at', 'opening_cash', 'closing_cash', 'is_active']

    # -- -- -- -- --
    def validate_opening_cash(self, value):
        if value < 0:
            raise serializers.ValidationError("Kirim 0dan kichik bo'lishi mumkin emas")
        return value
    
    # -- -- -- -- --
    def validate_closing_cash(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Kirim 0dan kichik bo'lishi mumkin emas")
        return value

# -- -- -- -- -- -- -- -- -- --
class OrderAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderAuditLog
        fields = ['order', 'old_data', 'new_data', 'situation', 'description', 'editor']

# -- -- -- -- -- -- -- -- -- --
class EmployeeKPISerializer(serializers.ModelSerializer):
    class Meta:
        model  = EmployeeKPI
        fields = ['user', 'bonus_kpi', 'salary']

    # -- -- -- -- --
    def validate_bonus_kpi(self, value):
        if value < 0:
            raise serializers.ValidationError("Bonus manfiy bo'lishi mumkin emas")
        return value
    
    # -- -- -- -- --
    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Maosh manfiy bo'lishi mumkin emas")
        return value