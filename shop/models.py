from django.db import models
from core.models import BaseModel
from accounts.models import City
from django.utils import timezone
from core import DiscountType
from django.db.models import Q


class Category(BaseModel):
    title = models.CharField(max_length=100)    

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='image/products')
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("shop:detail", kwargs={"id": self.id, "title": self.title})


class SpecialPriceManager(models.Manager):
    def active(self):
        return super().get_queryset()


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
