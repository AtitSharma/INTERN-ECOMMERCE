from django import forms
from product.models import Product



class ProductCreationForm(forms.ModelForm):
    class Meta:
        model=Product
        # fields="__all__"
        exclude=("user",)


