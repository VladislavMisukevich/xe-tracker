from .models import Product
from django.shortcuts import render, redirect
from .forms import MealForm
from .models import Meal
from datetime import date
from django.utils import timezone
from collections import defaultdict
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder
import calendar
from datetime import datetime, timedelta
from django.http import JsonResponse

@login_required
def meals_on_date(request):
    date_str = request.GET.get('date')
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse([], safe=False)

    meals = Meal.objects.filter(user=request.user, date=date_obj)
    data = [{"product_name": m.product_name, "weight": m.weight} for m in meals]
    return JsonResponse(data, safe=False)


@login_required
def custom_calendar_view(request):
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    cal = calendar.Calendar(firstweekday=0)
    calendar_weeks = cal.monthdatescalendar(year, month)

    meals = Meal.objects.filter(user=request.user, date__year=year, date__month=month)
    meals_by_date = defaultdict(list)
    for meal in meals:
        meals_by_date[meal.date].append(meal)

    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'calendar_weeks': calendar_weeks,
        'meals_by_date': meals_by_date,
        'weekdays': weekdays,
    }
    return render(request, 'main/custom_calendar.html', context)



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
            result = round((product.carbs_per_100g * weight) / 1000, 2)
        except (ValueError, Product.DoesNotExist):
            result = "Продукт не найден"

    return render(request, 'main/calculator.html', {
        'products': products,
        'result': result
    })

# Справочник продуктов с поиском и сортировкой
def product_list_view(request):
    sort_by = request.GET.get('sort')
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if sort_by in ['name', '-name', 'carbs', '-carbs']:
        order_field = 'carbs_per_100g' if 'carbs' in sort_by else 'name'
        products = products.order_by(sort_by.replace('carbs', 'carbs_per_100g'))

    return render(request, 'main/product_list.html', {
        'products': products
    })

@login_required
def add_meal_view(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user

            # Расчёт углеводов (carbs) и ХЕ (xe)
            meal.carbs = (meal.weight / 100) * 12  # Пример: 12 г углеводов на 100 г
            meal.xe = meal.carbs / 12

            meal.save()
            return redirect('meal_calendar')
    else:
        form = MealForm()

    return render(request, 'main/add_meal.html', {'form': form})
