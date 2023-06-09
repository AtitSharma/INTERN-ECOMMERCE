from django.urls import path
from product.views import (Shop,SellItem,ProductDetailView,Search,EditProductView,
                           add_to_cart,add_to_wishlist,DeleteCart,MyProductView,try_ajax,
                           MyWishList,HomeView,MyCart,like,DeleteCommentView)



app_name="product"
urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path('shop/',Shop.as_view(),name="shop1"),
    path('shop/<int:cartid>/',Shop.as_view(),name="shop"),
    path('my-cart/<str:username>/',MyCart.as_view(),name="my_cart"),
    path('add-to-cart/<int:pk>/',add_to_cart,name="add_to_cart"),
    path("sell-item/",SellItem.as_view(),name="sell-product"),
    path("add-wishlist/<str:username>/<int:pid>/",add_to_wishlist,name="add-wishlist"),
    path("my-wishlist/<str:username>/",MyWishList.as_view(),name="wishlist"),
    path("product/<int:pk>/",ProductDetailView.as_view(),name="product_detail"),
    path("delete-cart/<str:username>/<int:cid>/",DeleteCart.as_view(),name="delete-cart"),
    path("search/",Search.as_view(),name="search"),
    path("like/<int:pid>/",like,name="like"),
    path("delete-comment/<int:id>/",DeleteCommentView.as_view(),name="delete-comment"),
    path("my_product/",MyProductView.as_view(),name="my_products"),
    path("edit-product/<int:pk>/",EditProductView.as_view(),name="edit_product"),
    path("try/",try_ajax,name="ajax")
    
    
    
]
