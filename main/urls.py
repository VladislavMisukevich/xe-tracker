from django.urls import path
from .views import (
    home_view,
    calculator_view,
    product_list_view,
    about_view,
)

urlpatterns = [
    path('', home_view, name='home'),  # Главная страница
    path('calculator/', calculator_view, name='calculator'),  # Калькулятор ХЕ
    path('products/', product_list_view, name='product_list'),  # Справочник продуктов
    path('about/', about_view, name='about'),  # О проекте
]
