from django.contrib import admin
from . import views
from .models import Product, Waste

# -- -- -- -- -- -- -- -- -- --
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'unit', 'quantity', 'price')
    search_fields = ('name',)
    list_filter   = ('unit',)

# -- -- -- -- -- -- -- -- -- --
@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    list_display  = ('menu_item', 'product', 'quantity', 'description', 'reason', 
                     'responsible_person', 'created_at')
    search_fields = ('menu_item__name', 'product__name')
    list_filter   = ('reason', 'responsible_person__user__username')

