from django import forms
from product.models import Product,Comment



class ProductCreationForm(forms.ModelForm):
    class Meta:
        model=Product
        exclude=("user",)
        
class ProductSearchForm(forms.Form):
    product_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':"Enter the product name"}))

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["details"]
