from django.db import models
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
        from discount.utils import get_special_price

        max_special_price = get_special_price(self)
        if max_special_price['percent_type'] is None and max_special_price['fixed_type'] is None:
            return self.price

        fixed_price = self.price
        percent_price = self.price

        if max_special_price.get('fixed_type'):
            fixed = max_special_price['fixed']
            fixed_price = max(self.price - fixed, 0)

        if max_special_price.get('percent_type'):
            percent = int(self.price * (max_special_price['percent'] / 100))
            percent_price = max(self.price - percent, 0)

        return min(fixed_price, percent_price)
