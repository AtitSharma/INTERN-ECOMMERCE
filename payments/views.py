from django.shortcuts import render
from my_inventory.models import Inventory
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from product.models import Product,Cart
from django.contrib import messages


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):        
        price = Product.objects.get(id=self.kwargs["pk"])
        try:
            cart=Cart.objects.get(product__id=price.id,username=request.user.username)
            if cart.product.user==request.user:
                messages.add_message(request,messages.ERROR,"Unable to buy your own product")
                return redirect("product:home")
            quantity=cart.quantity
        except:
            if price.user == request.user:
                messages.add_message(request,messages.ERROR,"Unable to buy your own product")
                return redirect("product:home")               
            quantity=1
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items = [
                {
                    'price_data':{
                        'currency':'NPR',
                        'unit_amount': price.price * 100,
                        'product_data':{
                            'name': request.user.username,
                        }
                    },
                    'quantity': quantity
                },
            ],
            metadata = {"productid":price.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL+ str(price.id))     
        return redirect(checkout_session.url)



class SuccessView(TemplateView,View):
    template_name = "home.html" 
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("id")
        if product_id:
            product=Product.objects.get(id=product_id)
            try:
                cart=Cart.objects.get(product__id=product.id,username=request.user.username)
                if product.quantity < cart.quantity:
                    messages.add_message(request,messages.INFO,"Cannot purchased the product please Select less amout")
                    return redirect("product:home")
                product.quantity -= cart.quantity
                product.save()
                inventory=Inventory.objects.create(user=product.user,buyer_user=request.user,quantity=cart.quantity)
                inventory.save()
                product=Product.objects.get(id=product_id)
                inventory.product.add(product)
                print(inventory.product.all())
                cart.delete()
                messages.add_message(request,messages.INFO,"Sucessfully  purchased the product")
                return redirect("product:home")
            except:
                quantity=1
                if product.quantity < quantity:
                    messages.add_message(request,messages.INFO,"Cannot purchased the product please Select less amout")
                    return redirect("product:home")
                product.quantity -= quantity
                product.save()
                inventory=Inventory.objects.create(user=product.user,buyer_user=request.user,quantity=quantity)
                inventory.save()
                inventory.product.add(product)
                
                messages.add_message(request,messages.INFO,"Sucessfully  purchased the product")
                return redirect("product:home")    
        else:
            messages.add_message(request,messages.INFO,"Unable to purchase the product")
            return redirect("product:home")





    
