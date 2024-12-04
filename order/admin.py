from django.contrib import admin
from . import models


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'quantity']

    def delete_queryset(self, request, queryset):
        for cart in queryset:
            cart.delete()


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status']
    list_filter = ['status']

    def delete_queryset(self, request, queryset):
        for order in queryset:
            order.delete()


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'product', 'quantity', 'price']

    def delete_queryset(self, request, queryset):
        for order_product in queryset:
            order_product.delete()


admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderProduct, OrderProductAdmin)
