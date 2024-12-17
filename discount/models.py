from django.db import models
from shop.models import Category, Product
from core.models import BaseModel
from django.utils import timezone
from core import DiscountType
from django.db.models import F, Q


class DiscountManager(models.Manager):
    def active(self, date=None):
        if date is None:
            date = timezone.now()
        return self.filter(
            Q(end_time__isnull=True) | Q(end_time__gte=date), start_time__lte=date
        )

    def expired(self, date=None):
        if date is None:
            date = timezone.now()
        return self.filter(end_time__lt=date, start_time_lt=date)


class SpecialPrice(BaseModel):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=DiscountType.CHOICES, default=DiscountType.FIXED)
    value = models.PositiveIntegerField()

    objects = DiscountManager()

    def __str__(self):
        return self.name


class DiscountCode(BaseModel):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=DiscountType.CHOICES, default=DiscountType.FIXED)
    value = models.PositiveIntegerField()

    objects = DiscountManager()

    def __str__(self):
        return self.name
