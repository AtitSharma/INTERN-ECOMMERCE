from django.urls import path
from product.views import (Shop,SellItem,ProductDetailView,search,
                           add_to_cart,add_to_wishlist,DeleteCart,
                           MyWishList,HomeView,MyCart)



app_name="product"
urlpatterns = [
    path("home/",HomeView.as_view(),name='home'),
    path('shop/',Shop.as_view(),name="shop1"),
    path('shop/<int:cartid>/',Shop.as_view(),name="shop"),
    path('my-cart/<str:username>/',MyCart.as_view(),name="my_cart"),
    path('add-to-cart/<int:pk>/',add_to_cart,name="add_to_cart"),
    path("sell-item/",SellItem.as_view(),name="sell-product"),
    path("add-wishlist/<str:username>/<int:pid>/",add_to_wishlist,name="add-wishlist"),
    path("my-wishlist/<str:username>/",MyWishList.as_view(),name="wishlist"),
    path("product/<int:pk>/",ProductDetailView.as_view(),name="product_detail"),
    path("delete-cart/<str:username>/<int:cid>/",DeleteCart.as_view(),name="delete-cart"),
    path("search/",search,name="search"),
    
    
    
]
