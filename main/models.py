from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

def current_time():
    return datetime.now().time()

class Product(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="🍎 Название продукта"
    )
    carbs_per_100g = models.FloatField(
        verbose_name="🥖 Углеводы на 100 г"
    )

    def __str__(self):
        return self.name

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name="🥣 Вес (г)")
    carbs = models.FloatField(blank=True, null=True, verbose_name="🍬 Углеводы (г)")
    xe = models.FloatField(blank=True, null=True, verbose_name="🍞 Хлебные единицы")
    date = models.DateField(default=timezone.now, verbose_name="📅 Дата")
    time = models.TimeField(default=current_time, verbose_name="⏰ Время")

    def __str__(self):
        return f"{self.product.name} — {self.date} ({self.user.username})"

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"
        ordering = ['-date', '-time']
