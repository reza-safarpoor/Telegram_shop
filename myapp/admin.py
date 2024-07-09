from django.contrib import admin
from .models import Products, TelegramUser, Payment

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Platform', 'Price')
    search_fields = ('Name',)
    list_filter = ('Platform',)

admin.site.register(TelegramUser)
admin.site.register(Payment)