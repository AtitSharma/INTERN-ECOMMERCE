from django.contrib import admin
from product.models import Product,Cart,Category

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["name","image1","image2","description","price","user","category","quantity","status"]
    
# admin.site.register(Product,ProductAdmin)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=["name","image","description"]
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=["username","product","quantity","total_price"]

   
