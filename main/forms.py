from django import forms
from .models import Meal, Product

class MealForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label='Продукт',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Meal
        fields = ['date', 'time', 'product', 'weight']
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
