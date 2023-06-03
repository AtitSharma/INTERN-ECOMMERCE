from django.urls import path
from payments.views import CreateStripeCheckoutSessionView, SuccessView

app_name = "payments"
urlpatterns = [
    path('create-checkout-session/<int:pk>/',CreateStripeCheckoutSessionView.as_view(),name="create-checkout-session",),
    path('success/',SuccessView.as_view(), name="success")
]