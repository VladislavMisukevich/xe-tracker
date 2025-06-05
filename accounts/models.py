from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # ваши поля, например:
    LIFESTYLE_CHOICES = [
        ('low', 'Малоподвижный без лишнего веса (15–18 ХЕ)'),
        ('active', 'Активный образ жизни (до 30 ХЕ)'),
        ('overweight', 'Лишний вес + низкая активность (до 12 ХЕ)'),
    ]
    lifestyle = models.CharField(
        max_length=20,
        choices=LIFESTYLE_CHOICES,
        default='low',
        verbose_name='Образ жизни',
    )

    def get_daily_xe_norm(self):
        if self.lifestyle == 'low':
            return 18
        elif self.lifestyle == 'active':
            return 30
        elif self.lifestyle == 'overweight':
            return 12
        return 18  # значение по умолчанию
