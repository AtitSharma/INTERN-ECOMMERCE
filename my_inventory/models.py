from django.db import models
from django.conf import settings
from product.models import Product


class Inventory(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    buyer_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="inventory_buyer")
    product=models.ManyToManyField(Product)
    
    