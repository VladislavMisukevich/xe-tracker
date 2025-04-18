from django.shortcuts import render
from .models import Product

def home_view(request):
    return render(request, 'main/home.html')

def about_view(request):
    return render(request, 'main/about.html')


def calculator_view(request):
    result = None
    products = Product.objects.all()

    if 'product' in request.GET and 'weight' in request.GET:
        name = request.GET['product']
        weight = float(request.GET['weight'])
        try:
            product = Product.objects.get(name__iexact=name)
            result = round((product.carbs_per_100g * weight) / 1000, 2)
        except Product.DoesNotExist:
            result = "Продукт не найден"

    return render(request, 'main/calculator.html', {
        'products': products,
        'result': result
    })

def product_list_view(request):
    sort_by = request.GET.get('sort')
    query = request.GET.get('q')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == '-name':
        products = products.order_by('-name')
    elif sort_by == 'carbs':
        products = products.order_by('carbs_per_100g')
    elif sort_by == '-carbs':
        products = products.order_by('-carbs_per_100g')

    return render(request, 'main/product_list.html', {
        'products': products
    })


# Create your views here.
