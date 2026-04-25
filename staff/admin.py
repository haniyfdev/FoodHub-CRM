from django.contrib import admin
from .models import Shift, OrderAuditLog, EmployeeKPI

# -- -- -- -- -- -- -- -- -- --
@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display  = ('cashier', 'opened_at', 'closed_at', 'opening_cash','closing_cash', 'is_active')
    search_fields = ('cashier__username',)
    list_filter   = ('is_active',)
    readonly_fields = ('opened_at',) # Ochilgan vaqtni o'zgartirib bo'lmaydi

# -- -- -- -- -- -- -- -- -- --
@admin.register(OrderAuditLog)
class OrderAuditLogAdmin(admin.ModelAdmin):
    list_display  = ('order', 'old_data', 'new_data', 'situation', 'editor')
    search_fields = ('order__unique_num', 'editor__username')
    list_filter   = ('situation',)
    # Audit loglar umuman o'zgarmasin
    readonly_fields = ('order', 'old_data', 'new_data', 
                       'situation', 'editor', 'restaurant')
    # Admin panelda yangi log qo'shilmasin
    def has_add_permission(self, request):
        return False

# -- -- -- -- -- -- -- -- -- --
@admin.register(EmployeeKPI)
class EmployeeKPIAdmin(admin.ModelAdmin):
    list_display  = ('user', 'bonus_kpi', 'salary')
    search_fields = ('user__username',)
    

