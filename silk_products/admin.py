from django.contrib import admin
from .models import SilkProduct

@admin.register(SilkProduct)
class SilkProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'availability')
    list_filter = ('type', 'availability')
    search_fields = ('name', 'type')
