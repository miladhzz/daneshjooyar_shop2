from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from core.models import City


class SoftUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    deleted = models.BooleanField(default=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_email_verified = models.BooleanField(default=False)

    objects = SoftUserManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
