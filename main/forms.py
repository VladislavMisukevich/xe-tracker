from django import forms
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['date', 'time', 'product_name', 'weight']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
        labels = {
            'date': 'Дата',
            'time': 'Время',
            'product_name': 'Продукт',
            'weight': 'Вес (г)',
        }
