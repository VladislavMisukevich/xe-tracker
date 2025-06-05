from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Импортируй свою модель

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'lifestyle']  # Добавь сюда нужные поля

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🏷️ Устанавливаем русские названия полей
        self.fields['username'].label = "Имя пользователя"
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"
        self.fields['lifestyle'].label = "Образ жизни"

        # 🎨 Применяем стили Bootstrap
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.label_suffix = ''  # Убираем двоеточие

