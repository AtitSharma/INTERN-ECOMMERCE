from django.shortcuts import render

# Create your views here.
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
        cart=Cart.objects.get(product__id=price.id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items = [
                {
                    'price_data':{
                        'currency':'NPR',
                        'unit_amount': price.price * 100,
                        'product_data':{
                            'name': price.user.email,
                        }
                    },
                    'quantity': cart.quantity
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
            cart=Cart.objects.get(product__id=product.id)
            if product.quantity < cart.quantity:
                messages.add_message(request,messages.INFO,"Cannot purchased the product please Select less amout")
                return redirect("product:home")
            product.quantity -= cart.quantity
            product.save()
            messages.add_message(request,messages.INFO,"Sucessfully  purchased the product")
            return redirect("product:home")
        else:
            messages.add_message(request,messages.INFO,"Unable to purchase the product")
            return redirect("product:home")





    
