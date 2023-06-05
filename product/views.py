
from django.shortcuts import render,redirect,reverse
from product.models import Category,Cart,Product,Wishlist,Like,Comment
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponseRedirect,HttpResponse
from product.forms import ProductCreationForm,ProductSearchForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.http import Http404





class HomeView(View):  
    def get(self,request):
        context={
            "categories":Category.objects.all(),
            "products":Product.objects.filter(quantity__gte=1),
            "form":ProductSearchForm,
        }
        return render(request,"home.html",context)
    
class Shop(View):
    def get(self,request,cartid=None):
        categories=Category.objects.all()
        if cartid==None:
            products=Product.objects.filter(quantity__gte=1)
            context={
                "products":products,
                'categories':categories        
                }
            return render(request,'shop.html',context)
        products=Product.objects.filter(category__id=cartid,quantity__gte=1)
        context={
            'products':products,
            'categories':categories
        }
        return render(request,'shop.html',context)
        
            


class MyCart(LoginRequiredMixin,View):
    def get(self,request,username):
        if request.user.username != username:
            return redirect("product:home")
        context={
            "carts":Cart.objects.filter(username=username)
        }
        return render(request,"my_cart.html",context)


@login_required
def add_to_cart(request,pk,quantity=1):
    username=request.user.username
    product=Product.objects.get(pk=pk)
    price=Product.objects.get(pk=pk).price
    total_price=quantity*price
    if Cart.objects.filter(username=username,product__name=product).exists():
        cart_item=Cart.objects.get(username=username,product__name=product)
        cart_item.quantity +=quantity
        cart_item.total_price += total_price
        cart_item.save()
        messages.add_message(request,messages.INFO,f"Sucessfully Updated Cart {product}")
        return HttpResponseRedirect(reverse("product:my_cart",args=(request.user.username,)))
    else:
        Cart.objects.create(username=username,product=product,quantity=quantity,total_price=total_price)
        messages.add_message(request,messages.INFO,f"Sucessfully Added {product} in Cart")
    return HttpResponseRedirect(reverse("product:my_cart",args=(request.user.username,)))
    
class SellItem(LoginRequiredMixin,View):
    def get(self,request):
        form=ProductCreationForm()
        return render(request,"product_creation.html",{"form":form})
    def post(self,request):
        form=ProductCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.user=request.user
            user.save()
            return redirect("product:home")
        
        
        

@login_required
def add_to_wishlist(request,username,pid):
    if request.user.username !=username:
        return redirect("product:home")
    product=Product.objects.get(id=pid)
    if Wishlist.objects.filter(username=username,product__id=pid).exists():
        wishlist=Wishlist.objects.get(username=username,product__id=pid)
        wishlist.delete()
        messages.add_message(request,messages.INFO,"Sucessfully removed from wishlist")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        Wishlist.objects.create(username=username,product=product)
        messages.add_message(request,messages.INFO,"Sucessfully added to wishlist")
        return redirect(request.META.get('HTTP_REFERER'))

class MyWishList(LoginRequiredMixin,View):
    def get(self,request,username):
        if request.user.username != username:
            return redirect("product:home")
        wishlist=Wishlist.objects.filter(username=username)
        context={
            "wishlist":wishlist,
        }
        return render(request,"wishlist.html",context)
    
        
class ProductDetailView(DetailView):
    model=Product
    template_name="product_detail.html"
    
    def get_context_data(self, **kwargs):
        pk=self.kwargs.get("pk")
        context=super().get_context_data(**kwargs)
        context["likes"]=Like.objects.filter(product__id=pk,is_liked=True)
        return context
    
class DeleteCart(View):
    def get(self,request,username,cid):
        if request.user.username != username:
            raise Http404
        cart=Cart.objects.filter(username=username,id=cid)
        cart.delete()
        return redirect("product:my_cart",username=username)
    
    
def search(request):
    name=request.POST.get('product_name').upper()
    products=Product.objects.filter(name__icontains=name)
    if not products:
        return HttpResponse('Not Found')
    return render(request,"search.html",{"products":products})

    
    
    

def like(request,pid):
    product = Product.objects.get(id=pid)
    like, created = Like.objects.get_or_create(user=request.user, product=product)

    if created or not like.is_liked:
        like.is_liked = True
    else:
        like.is_liked = False

    like.save()
    return HttpResponseRedirect(reverse("product:product_detail",kwargs={"pk":pid}))