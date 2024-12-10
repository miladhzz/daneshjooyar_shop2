from django.db import models
from core import DiscountType
from core.models import BaseModel
from accounts.models import City


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

    def get_price(self, special_price):
        if special_price is None:
            return None

        if special_price['type'] == DiscountType.FIXED:
            if self.price < special_price['fixed']:
                return self.price
            return self.price - special_price['fixed']

        discount_amount = self.price * (special_price['percent'] / 100)
        return self.price - discount_amount
