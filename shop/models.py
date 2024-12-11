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
        if special_price['percent_type'] is None and special_price['fixed_type'] is None:
            return None

        fixed_price = 0
        percent_price = 0

        if special_price['fixed_type']:
            if self.price < special_price['fixed']:
                fixed_price = self.price
            else:
                fixed_price = self.price - special_price['fixed']

        if special_price['percent_type']:
            discount_amount = self.price * (special_price['percent'] / 100)
            percent_price = self.price - discount_amount

        if fixed_price < percent_price:
            return fixed_price
        else:
            return percent_price
