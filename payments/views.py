from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from product.models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        price = Product.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items = [
                {
                    'price_data':{
                        'currency':'usd',
                        'unit_amount': price.price * 100,
                        'product_data':{
                            'name': price.user.email,
                        }
                    },
                    'quantity': 1
                },
            ],
            metadata = {"productid":price.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            
        )
        
        return redirect(checkout_session.url)
    


class SuccessView(TemplateView):
    template_name = "success.html"
