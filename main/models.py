from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # ← ЭТО ДОБАВЛЕНО

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateField(default=timezone.localdate)  # ← использует локальную дату
    time = models.TimeField(null=True, blank=True, verbose_name="Время приёма пищи")
    product_name = models.CharField(max_length=100, verbose_name="Продукт")
    weight = models.FloatField(verbose_name="Вес (г)")
    carbs = models.FloatField(verbose_name="Углеводы (г)")
    xe = models.FloatField(verbose_name="ХЕ")

    def __str__(self):
        return f"{self.product_name} — {self.date} ({self.user.username})"

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"
        ordering = ['-date', '-time']


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
