from django.conf import settings
from django.utils import timezone
from django.db import models
from datetime import datetime
from django_ckeditor_5.fields import CKEditor5Field

# ⏰ Текущее время по умолчанию для поля "Время"
def current_time():
    return datetime.now().time()

# 🍎 Продукты
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

# 🍽 Приём пищи
class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name="🥣 Вес (г)")
    carbs = models.FloatField(blank=True, null=True, verbose_name="🍬 Углеводы (г)")
    xe = models.FloatField(blank=True, null=True, verbose_name="🍞 Хлебные единицы")
    date = models.DateField(default=timezone.now, verbose_name="📅 Дата")
    time = models.TimeField(default=current_time, verbose_name="⏰ Время")

    def __str__(self):
        return f"{self.product.name} — {self.date} ({self.user.username})"

    def get_xe(self):
        """Подсчёт ХЕ из углеводов"""
        if self.carbs is not None:
            return round(self.carbs / 12, 2)
        return None

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"
        ordering = ['-date', '-time']

# 📚 Статьи
class Article(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    summary = models.TextField("Краткое описание", max_length=300, blank=True)
    content = CKEditor5Field("Содержимое", config_name='default')
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']
