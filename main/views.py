from django.shortcuts import render
from .models import Product

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
