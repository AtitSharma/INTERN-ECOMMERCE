from django import forms
from product.models import Product



class ProductCreationForm(forms.ModelForm):
    class Meta:
        model=Product
        # fields="__all__"
        exclude=("user",)
        
class ProductSearchForm(forms.Form):
    product_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':"Enter the product name"}))


