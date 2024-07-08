from django.contrib import admin
from .models import Products, TelegramUser

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Platform', 'Price')
    search_fields = ('Name',)
    list_filter = ('Platform',)

admin.site.register(TelegramUser)