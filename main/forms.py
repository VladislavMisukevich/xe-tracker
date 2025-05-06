from django import forms
from .models import Meal, Product

class MealForm(forms.ModelForm):
    product_name = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label='Продукт',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Meal
        fields = ['date', 'time', 'product_name', 'weight']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
        labels = {
            'date': 'Дата',
            'time': 'Время',
            'weight': 'Вес (г)',
        }
