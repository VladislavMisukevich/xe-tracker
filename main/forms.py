from django import forms
from .models import Meal, Product

class MealForm(forms.ModelForm):
    product = forms.CharField(
        label='Продукт',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'product-list',
            'autocomplete': 'off',
        })
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

    def clean_product(self):
        name = self.cleaned_data['product']
        try:
            return Product.objects.get(name__iexact=name)
        except Product.DoesNotExist:
            raise forms.ValidationError("Такой продукт не найден. Пожалуйста, выберите из списка.")
