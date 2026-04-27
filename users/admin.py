from django.contrib import admin
from .models import Profile, Restaurant

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'avatar', 'role', 'phone', 'pasport')
    search_fields = ('user__username', 'phone')
    list_filter   = ('role',)

@admin.register(Restaurant)    
class RestaurantAdmin(admin.ModelAdmin):
    list_display =  ('name', 'address', 'created_at', 'password', 'is_active', 'paid_until')
    search_fields = ('name', 'address')

