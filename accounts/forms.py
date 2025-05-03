from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🏷️ Устанавливаем русские названия полей
        self.fields['username'].label = "Имя пользователя"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"

        # 🎨 Применяем стили Bootstrap и убираем лишнее
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.label_suffix = ''  # Убираем двоеточие после метки
