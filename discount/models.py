from django.db import models
from shop.models import Category, Product
from core.models import BaseModel
from django.utils import timezone
from core import DiscountType


class DiscountPrice(BaseModel):
    name = models.CharField(max_length=255)
    product = models.ManyToManyField(Product, null=True, blank=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=DiscountType.CHOICES, default=DiscountType.FIXED)
    percent = models.PositiveIntegerField(null=True, blank=True)
    fixed = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name
