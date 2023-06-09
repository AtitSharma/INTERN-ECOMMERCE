from django.urls import path
from my_inventory.views import MyInventoryView


app_name="inventory"

urlpatterns = [
    path("",MyInventoryView.as_view(),name="my_inv"),
]
