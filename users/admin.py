from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'avatar', 'role', 'phone', 'pasport')
    search_fields = ('user__username', 'phone')
    list_filter   = ('role',)

    
