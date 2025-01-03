from django.db import models
from core.models import BaseModel
from shop.models import Product, Category
from core import DiscountType
from django.utils import timezone
from django.db.models import Q


class DiscountManager(models.Manager):
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

    objects = DiscountManager()

    def __str__(self):
        return self.name


class DiscountCode(BaseModel):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    discount_code_type = models.CharField(max_length=7, choices=DiscountType.CHOICES, default=DiscountType.FIXED)
    discount_code_value = models.PositiveIntegerField()

    objects = DiscountManager()

    def __str__(self):
        return self.name

    def get_discount(self, price):
        if self.discount_code_type == DiscountType.FIXED:
            return max(price - self.discount_code_value, 0)

        percent = int(price * (self.discount_code_value / 100))
        return max(price - percent, 0)
