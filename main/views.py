from datetime import datetime
from collections import defaultdict
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

from .models import Product, Meal, Article
from .forms import MealForm
from .forms import ProductForm

import calendar
from datetime import date

# Главная страница
def home_view(request):
    return render(request, 'main/home.html')


# Страница "О проекте"
def about_view(request):
    return render(request, 'main/about.html')


# Калькулятор хлебных единиц
def calculator_view(request):
    result = None
    products = Product.objects.all()

    if 'product' in request.GET and 'weight' in request.GET:
        name = request.GET['product']
        try:
            weight = float(request.GET['weight'])
            product = Product.objects.get(name__iexact=name)
            result = round(product.carbs_per_100g * weight / 1000, 2)
        except (ValueError, Product.DoesNotExist):
            result = "Продукт не найден"

    return render(request, 'main/calculator.html', {
        'products': products,
        'result': result
    })


# Список продуктов
def product_list_view(request):
    sort_by = request.GET.get('sort')
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if sort_by in ['name', '-name', 'carbs', '-carbs']:
        products = products.order_by(sort_by.replace('carbs', 'carbs_per_100g'))

    return render(request, 'main/product_list.html', {
        'products': products
    })


# Добавление приёма пищи
@login_required
def add_meal_view(request):
    initial_date = request.GET.get('date')

    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.product = form.cleaned_data['product']  # возвращается Product из clean_product
            if meal.product and meal.weight:
                meal.carbs = round((meal.product.carbs_per_100g * meal.weight) / 100, 2)
                meal.xe = round(meal.carbs / 12, 2)
            meal.save()
            return redirect('custom_calendar')
    else:
        form = MealForm(initial={'date': initial_date})

    products = Product.objects.all()
    return render(request, 'main/add_meal.html', {'form': form, 'products': products})


# Детальный просмотр приёма пищи
@login_required
def meal_detail_view(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    return render(request, 'main/meal_detail.html', {'meal': meal})


# Приёмы пищи на конкретную дату (AJAX)
@login_required
def meals_on_date(request):
    date_str = request.GET.get('date')
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse([], safe=False)

    meals = Meal.objects.filter(user=request.user, date=date_obj)
    data = [{"id": m.id, "product_name": m.product.name, "weight": m.weight} for m in meals]
    return JsonResponse(data, safe=False)


# Календарь с приёмами пищи (новый)
@login_required
def custom_calendar_view(request):
    # Получаем дату
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    # Корректировка на переход между годами
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    # Генерация структуры календаря
    cal = calendar.Calendar(firstweekday=0)
    calendar_weeks = cal.monthdatescalendar(year, month)

    # Запрос приёмов пищи пользователя
    meals = Meal.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    )

    # Распределение по дням
    meals_by_date = defaultdict(list)
    xe_by_date = defaultdict(float)
    for meal in meals:
        date_str = meal.date.isoformat()
        meals_by_date[date_str].append(meal)
        xe_by_date[date_str] += meal.get_xe()

    # Округляем ХЕ
    for date_str in xe_by_date:
        xe_by_date[date_str] = round(xe_by_date[date_str], 2)

    # Подготовка данных для графика
    num_days = calendar.monthrange(year, month)[1]
    day_labels = [str(day) for day in range(1, num_days + 1)]
    xe_values = []
    for day in range(1, num_days + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        xe = xe_by_date.get(date_str, 0)
        xe_values.append(float(xe))

    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    daily_xe_norm = request.user.get_daily_xe_norm()
    month_name = calendar.month_name[month]

    context = {
        'year': year,
        'month': month,
        'month_name': month_name,
        'calendar_weeks': calendar_weeks,
        'meals_by_date': meals_by_date,
        'xe_by_date': xe_by_date,
        'daily_xe_norm': daily_xe_norm,
        'weekdays': weekdays,
        'day_labels': day_labels,
        'xe_values': xe_values,
    }

    return render(request, 'main/custom_calendar.html', context)



# Календарь с приёмами пищи (старый FullCalendar)
@login_required
def meal_calendar_view(request):
    meals = Meal.objects.filter(user=request.user).order_by('-date', '-time')
    events = [
        {
            "title": f"{meal.product_name} — {meal.weight} г",
            "start": meal.date.isoformat(),
        }
        for meal in meals
    ]
    return render(request, 'main/meal_calendar.html', {
        'meals_json': json.dumps(events, cls=DjangoJSONEncoder)
    })

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'main/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'main/article_detail.html', {'article': article})

@login_required
def delete_meal(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    meal.delete()
    return redirect('custom_calendar')
