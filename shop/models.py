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

    @property
    def get_price(self):
        from discount.utils import get_max_special_price

        special_price = get_max_special_price(self)
        if special_price['percent_type'] is None and special_price['fixed_type'] is None:
            return None

        fixed_price = self.price
        percent_price = self.price

        if special_price.get('fixed_type'):
            fixed_discount = special_price['fixed']
            fixed_price = max(self.price - fixed_discount, 0)

        if special_price.get('percent_type'):
            percent_discount = int(self.price * (special_price['percent'] / 100))
            percent_price = max(self.price - percent_discount, 0)

        final_price = min(fixed_price, percent_price)
        return final_price if final_price < self.price else None

