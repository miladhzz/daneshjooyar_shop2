from django.db import models


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


class Province(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class City(models.Model):
    province = models.ForeignKey(Province, models.CASCADE)
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title
