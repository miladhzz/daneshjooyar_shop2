from django.db import models
from core.models import BaseModel
from shop.models import Product, Category
from core import DiscountType
from django.utils import timezone
from django.db.models import Q


class SpecialPriceManager(models.Manager):
    def active(self):
        date = timezone.now()
        return self.filter(Q(end_time__isnull=True) | Q(end_time__gte=date), start_time__lte=date)


class SpecialPrice(BaseModel):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    special_price_type = models.CharField(max_length=7, choices=DiscountType.CHOICES, default=DiscountType.FIXED)
    special_price_value = models.PositiveIntegerField()

    objects = SpecialPriceManager()

    def __str__(self):
        return self.name
