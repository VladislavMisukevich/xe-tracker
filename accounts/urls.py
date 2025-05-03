from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Регистрация нового пользователя
    path('register/', views.register, name='register'),

    # Вход в аккаунт
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    # Выход из аккаунта
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'  # После выхода переадресация на главную
    ), name='logout'),

    # Профиль пользователя
    path('profile/', views.profile, name='profile'),
]
