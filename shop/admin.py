from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']

    def delete_queryset(self, request, queryset):
        for category in queryset:
            category.delete()


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'quantity', 'status']
    search_fields = ['title']
    list_filter = ['status']

    def delete_queryset(self, request, queryset):
        for product in queryset:
            product.delete()


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
