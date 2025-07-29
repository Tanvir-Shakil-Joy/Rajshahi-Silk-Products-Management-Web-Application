from django.contrib import admin
from .models import SilkProduct, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')


@admin.register(SilkProduct)
class SilkProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'owner', 'availability', 'created_at')
    list_filter = ('type', 'availability', 'created_at', 'owner')
    search_fields = ('name', 'type', 'owner__username')
    list_editable = ('availability',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'type', 'price', 'availability')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
