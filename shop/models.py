from django.db import models
from django.conf import settings
from accounts.models import City


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class BaseModel(models.Model):
    deleted = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()


class Category(BaseModel):
    title = models.CharField(max_length=100)    

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='image/products')
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("shop:detail", kwargs={"id": self.id, "title": self.title})


class Cart(BaseModel):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Order(BaseModel):
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField(null=True)
    note = models.CharField(max_length=200, blank=True)
    different_address = models.BooleanField(default=False, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    address = models.CharField(max_length=500)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=10)


class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)


class PaymentLog(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.PositiveIntegerField()
    order_id = models.PositiveIntegerField()
    status = models.CharField(max_length=100)
    error_code = models.CharField(max_length=200)
