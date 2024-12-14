from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'quantity']

    def delete_queryset(self, request, queryset):
        for cart in queryset:
            cart.delete()


admin.site.register(Cart, CartAdmin)
