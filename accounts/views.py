from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def register(request):
    """Регистрация нового пользователя с автоматическим входом."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход
            return redirect('home')  # Перенаправление после регистрации
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """Профиль авторизованного пользователя."""
    return render(request, 'accounts/profile.html')
