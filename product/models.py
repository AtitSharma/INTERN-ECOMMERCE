from django.db import models

# Create your models here.

from django.conf import settings



class Category(models.Model):
    name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='images',blank=True,null=True)
    description=models.TextField()
    
    def __str__(self):
        return str(self.name)
    
    
class Status(models.TextChoices):
    AVAILABLE="available",'AVAILABLE'
    SOLD='sold','SOLD'
    
    
class Product(models.Model):
    name=models.CharField(max_length=255)
    image1=models.ImageField(upload_to='images',blank=True,null=True)
    image2=models.ImageField(upload_to='images',blank=True,null=True)
    description=models.TextField()
    price=models.IntegerField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='product')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product')
    quantity=models.IntegerField()
    status=models.CharField(max_length=100,choices=Status.choices,default=Status.AVAILABLE)
    
    
    def __str__(self):
        return self.name
    
    
    
class Cart(models.Model):
    username=models.CharField(max_length=255)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart')
    quantity=models.IntegerField()
    total_price=models.IntegerField()
    
    
    
    def __str__(self):
        return str(self.username)
    
    
class Wishlist(models.Model):
    username=models.CharField(max_length=255)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlist')
    
    
class Like(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="like")
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="like")
    is_liked=models.BooleanField(default=False)

class Comment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="comment")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="comment")
    
    
    
    