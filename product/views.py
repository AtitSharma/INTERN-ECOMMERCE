
from django.shortcuts import render,redirect,reverse
from product.models import Category,Cart,Product,Wishlist,Like,Comment
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponseRedirect,HttpResponse
from product.forms import ProductCreationForm,ProductSearchForm,CommentCreationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json



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
        if product.quantity < cart_item.quantity:
            messages.add_message(request,messages.INFO,"Cannot Items more than available ")
            return redirect("product:home")
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
    
        
# class ProductDetailView(DetailView):
#     model=Product
#     template_name="product_detail.html"
    
#     def get_context_data(self, **kwargs):
#         pk=self.kwargs.get("pk")
#         context=super().get_context_data(**kwargs)
#         context["likes"]=Like.objects.filter(product__id=pk,is_liked=True)
#         context["form"]=CommentCreationForm()
#         context["comments"]=Comment.objects.filter(product__pk=pk)
#         return context
    
#     def post(self,request,*args,**kwargs):
#         pk=self.kwargs.get("pk")
#         product=Product.objects.get(id=pk)
#         form=CommentCreationForm(request.POST)
#         if form.is_valid():
#             comment=form.save(commit=False)
#             comment.user=request.user
#             comment.product=product
#             comment.save()
#             messages.add_message(request,messages.INFO,"Succesfuly added your Comment ")
            
#         return HttpResponseRedirect(reverse("product:product_detail",kwargs={"pk":pk}))
            

class ProductDetailView(View):
    
    
    def get(self,request,*args,**kwargs):
        pk=self.kwargs.get("pk")
        likes=Like.objects.filter(product__id=pk,is_liked=True)
        form=CommentCreationForm()
        comments=Comment.objects.filter(product__pk=pk)
        print(comments)
        product=Product.objects.get(id=pk)
        context={
            "likes":likes,
            "form":form,
            "comments":comments,
            "product":product,
            "id":pk,
        }
        return render(request,"product_detail.html",context)
       


    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk") 
        product = Product.objects.get(pk=pk)
        data = json.loads(request.body)
        
        form = CommentCreationForm(data)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            new_comment = {
                'user': {
                    'username': comment.user.username,
                    'email': comment.user.email,
                },
                'details': comment.details,
                'message':"Sucessfully Commented !!!",
                'id':comment.id
            }
            return JsonResponse({"comment": new_comment})


            
        
        
    
    
    


   
        
    
class DeleteCart(LoginRequiredMixin,View):
    def get(self,request,username,cid):
        if request.user.username != username:
            raise Http404
        cart=Cart.objects.filter(username=username,id=cid)
        cart.delete()
        return redirect("product:my_cart",username=username)
    
    
class Search(View):
    def post(self,request):
        name=request.POST.get('product_name').upper()
        products=Product.objects.filter(name__icontains=name)
        if not products:
            return HttpResponse('Not Found')
        return render(request,"search.html",{"products":products})

@login_required
def like(request,pid):
    product = Product.objects.get(id=pid)
    like, created = Like.objects.get_or_create(user=request.user, product=product)
    if created or not like.is_liked:
        like.is_liked = True
    else:
        like.is_liked = False
    like.save()
    return HttpResponseRedirect(reverse("product:product_detail",kwargs={"pk":pid}))

class DeleteCommentView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        comment_id=self.kwargs.get("id")
        comments=Comment.objects.filter(id=comment_id)
        print(comments)
        # product_id=Comment.objects.get(product_id=comment_id).product.id
        # comment=Comment.objects.get(id=comment_id)
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.user:
            messages.add_message(request,messages.INFO,"Cant Delete Other Comments")
            return redirect("product:product_detail",pk=comment.product.id)
        comment.delete()
        messages.add_message(request,messages.INFO,"Successfully deleted the comment")
        return redirect("product:product_detail",pk=comment.product.id)
    
    
        
        
class MyProductView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        products=Product.objects.filter(user__username=request.user.username,quantity__gte=1)
        context={
            "products":products,
        }
        return render (request,"my_products.html",context)
    
    

# def edit_product(request, pk):
#     product = Product.objects.get(pk=pk)
#     form = ProductCreationForm(instance=product)
#     if request.method == 'POST':
#         data=json.loads(request.body)
#         form = ProductCreationForm(data, instance=product) 
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'message': 'Product updated successfully'})

#     return render(request, "edit_product.html", {"form": form,"id":pk})



class EditProductView(LoginRequiredMixin,View,UserPassesTestMixin):
    
    def test_func(self,*args,**kwargs):
        pk=self.kwargs.get("pk")
        product=Product.objects.get(pk=pk)
        return self.request.user == product.user
    
    def get(self,request,*args,**kwargs):
        pk=self.kwargs.get("pk")
        if self.test_func(pk):
            pk=self.kwargs.get("pk")
            product = Product.objects.get(pk=pk)
            form = ProductCreationForm(instance=product)   
            return render(request,"edit_product.html",{"form":form,"id":pk})
        else:
            messages.add_message(request,messages.INFO,"Unable to edit other products")
            return redirect("product:home")
    
    def post(self,request,*kwargs,**args):
        data=json.loads(request.body)
        pk=self.kwargs.get("pk")
        product = Product.objects.get(pk=pk)
        form=ProductCreationForm(data,instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Product updated successfully'})
        
        
def try_ajax(request):
    d = {'testing': list({1, 2, 3})}
    if request.method=="POST":
        data = json.loads(request.body)
        print(data)
        
    return JsonResponse(data=d)



      
        
    
        
        


