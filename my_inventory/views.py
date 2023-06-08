from django.shortcuts import render

# Create your views here.
from django.views import View
from my_inventory.models import Inventory
from django.contrib.auth.mixins import LoginRequiredMixin


class MyInventoryView(LoginRequiredMixin,View):
    
    def get(self,request,*args,**kwargs):
        inverntories=Inventory.objects.filter(user=request.user)
        return render(request,"my_inventory.html",{"inventories":inverntories})
