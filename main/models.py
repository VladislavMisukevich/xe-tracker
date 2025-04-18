from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название продукта")
    carbs_per_100g = models.FloatField(verbose_name="Углеводы на 100г")

    def __str__(self):
        return self.name


# Create your models here.
