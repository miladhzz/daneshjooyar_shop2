from django.db import models
from core.models import BaseModel
from django.conf import settings
from shop.models import Product
from core.models import City
from core import OrderStatus


class Cart(BaseModel):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Order(BaseModel):
    total_price = models.IntegerField()
    discount_code = models.CharField(max_length=100, null=True)
    discount_id = models.IntegerField(null=True)
    total_discount = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=OrderStatus.CHOICES, default=OrderStatus.PENDING_PAYMENT)
    note = models.CharField(max_length=200, blank=True)
    different_address = models.BooleanField(default=False, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    address = models.CharField(max_length=500)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=10)
    zarinpal_authority = models.CharField(max_length=50, null=True)
    zarinpal_ref_id = models.IntegerField(null=True)


class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()
