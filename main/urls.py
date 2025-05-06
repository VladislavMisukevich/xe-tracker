from django.urls import path
from . import views
from .views import meal_detail_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('calculator/', views.calculator_view, name='calculator'),
    path('products/', views.product_list_view, name='product_list'),
    path('about/', views.about_view, name='about'),
    path('calendar/', views.meal_calendar_view, name='meal_calendar'),
    path('calendar/add/', views.add_meal_view, name='add_meal'),
    path('calendar/custom/', views.custom_calendar_view, name='custom_calendar'),
    path('api/meals/', views.meals_on_date, name='meals_on_date'),
    path('meal/<int:pk>/', meal_detail_view, name='meal_detail'),
]